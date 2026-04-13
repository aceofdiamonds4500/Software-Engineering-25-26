
import torch
import spacy
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict
from transformers import BertTokenizer, BertForMaskedLM

print('imports done')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')
model.eval()
print('BERT ready')

# source/docs - https://huggingface.co/docs/transformers/model_doc/bert#transformers.BertForMaskedLM

def get_predictions(sentence, top_k=5):
    # tokenize and find where the [MASK] tokens are
    inputs = tokenizer(sentence, return_tensors='pt')
    mask_positions = (inputs['input_ids'][0] == tokenizer.mask_token_id).nonzero(as_tuple=True)[0].tolist()

    if not mask_positions:
        print('No [MASK] found')
        return {}

    # run model
    with torch.no_grad():
        logits = model(**inputs).logits

    # for each mask, grab top-k predictions
    results = {}
    for pos in mask_positions:
        probs = torch.softmax(logits[0, pos], dim=-1)
        top_probs, top_ids = torch.topk(probs, top_k)
        results[pos] = [
            (tokenizer.decode([tid]).strip(), round(p.item(), 4))
            for tid, p in zip(top_ids, top_probs)
        ]
    return results


def show_predictions(sentence, top_k=5):
    print(f'Input:  {sentence}')
    print('-' * 55)

    results = get_predictions(sentence, top_k)
    filled = sentence

    for i, (pos, preds) in enumerate(results.items()):
        print(f'[MASK #{i+1}]')
        for rank, (word, prob) in enumerate(preds, 1):
            bar = '█' * int(prob * 40)
            print(f'  {rank}. {word:<15} {bar} {prob:.2%}')
        filled = filled.replace('[MASK]', preds[0][0], 1)
        print()

    print(f'Filled: {filled}\n')
    return filled

masked_sentences = [
    'The [MASK] sat on the mat.',
    'She quickly [MASK] to the store before it closed.',
    'The tall [MASK] building stood in the center of the city.',
    'He [MASK] a book about ancient [MASK].',
    'The scientist discovered a [MASK] method for solving the problem.'
]

filled_sentences = []
for s in masked_sentences:
    filled = show_predictions(s)
    filled_sentences.append(filled)
    print('=' * 55)

# source/docs for spacy en_core_web_sm - https://spacy.io/models/en#en_core_web_sm

nlp = spacy.load('en_core_web_sm')

def get_pos_tags(sentence):
    # returns list of (word, POS) pairs, skipping whitespace
    doc = nlp(sentence)
    return [(t.text, t.pos_) for t in doc if t.pos_ != 'SPACE']


def extract_transitions(sentences):
    # count how often each (tag_A -> tag_B) pair appears across all sentences
    counts = defaultdict(int)
    tagged = []

    for s in sentences:
        pairs = get_pos_tags(s)
        tags = [pos for _, pos in pairs]
        tagged.append((s, pairs))
        for i in range(len(tags) - 1):
            counts[(tags[i], tags[i+1])] += 1

    return counts, tagged


# combine BERT outputs with some extra sentences for more data
corpus = filled_sentences + [
    'The quick brown fox jumps over the lazy dog.',
    'She opened the old wooden door slowly.',
    'Birds fly south during the cold winter months.',
    'The curious student asked many difficult questions.',
    'He carefully placed the fragile glass on the table.',
    'They will travel to Paris next summer.',
    'The bright stars appeared in the dark night sky.',
    'A friendly dog ran through the green park.',
    'She reads interesting books every evening.',
    'The researchers published a groundbreaking study.'
]

transitions, tagged_corpus = extract_transitions(corpus)

# show a few examples
print('Sample POS sequences:')
print('-' * 55)
for sentence, pairs in tagged_corpus[:3]:
    tag_str = ' -> '.join(f'{w}/{t}' for w, t in pairs)
    print(f'  {sentence}')
    print(f'  {tag_str}\n')

print(f'Total unique transitions: {len(transitions)}')

'''
Key:
    DET — Determiner (the, a, this, my)
    NOUN — Noun (dog, city, book)
    VERB — Verb (runs, discovered, placed)
    ADP — Adposition meaning prepositions and postpositions (in, on, over, to, of)
    PUNCT — Punctuation (. , ! ?)
    PRON — Pronoun (he, she, they, it)
    ADV — Adverb (quickly, carefully, slowly)
    SCONJ — Subordinating Conjunction (before, because, although, while)
    ADJ — Adjective (quick, tall, bright)
    PROPN — Proper Noun (Paris, BERT, Google)
    AUX — Auxiliary Verb aka helper verbs (will, is, have, can)
'''
def build_fsm(transitions):
    G = nx.DiGraph()
    for (src, dst), count in transitions.items():
        if G.has_edge(src, dst):
            G[src][dst]['weight'] += count
        else:
            G.add_edge(src, dst, weight=count)
    return G


G = build_fsm(transitions)

print(f'States:      {list(G.nodes())}')
print(f'Num states:  {G.number_of_nodes()}')
print(f'Num edges:   {G.number_of_edges()}')
print()
print('All transitions (sorted by frequency):')
for src, dst, data in sorted(G.edges(data=True), key=lambda x: -x[2]['weight']):
    print(f'  {src:<10} -> {dst:<10}  count={data["weight"]}')

# color each POS state differently
POS_COLORS = {
    'NOUN': '#4A90D9', 'VERB': '#E85D5D', 'ADJ':  '#50C878',
    'ADV':  '#F0A500', 'DET':  '#9B59B6', 'PRON': '#1ABC9C',
    'ADP':  '#E67E22', 'PROPN':'#3498DB', 'PUNCT':'#95A5A6',
    'AUX':  '#E91E63', 'PART': '#FF5722', 'CCONJ':'#607D8B',
    'SCONJ':'#795548', 'NUM':  '#009688'
}


def draw_fsm(G, title='POS Transition FSM', min_weight=1):
    # drop low-frequency edges to keep the diagram readable
    H = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        if d['weight'] >= min_weight:
            H.add_edge(u, v, weight=d['weight'])
    for n in G.nodes():
        if n not in H:
            H.add_node(n)

    node_colors = [POS_COLORS.get(n, '#BDC3C7') for n in H.nodes()]

    # bigger node = more outgoing transitions
    node_sizes = []
    for n in H.nodes():
        total = sum(d['weight'] for _, _, d in H.out_edges(n, data=True))
        node_sizes.append(max(1500, total * 120))

    edge_weights = [H[u][v]['weight'] for u, v in H.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [1.0 + (w / max_w) * 4.0 for w in edge_weights]
    edge_labels = {(u, v): str(d['weight']) for u, v, d in H.edges(data=True)}

    layout = nx.spring_layout(H, seed=42, k=2.5)

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')

    nx.draw_networkx_edges(H, layout, ax=ax,
        edge_color='#aaaacc', width=edge_widths,
        arrows=True, arrowstyle='-|>', arrowsize=20,
        connectionstyle='arc3,rad=0.1', alpha=0.7)

    # double-circle the top 5 most active states
    top5 = sorted(H.nodes(), key=lambda n: sum(d['weight'] for _,_,d in H.out_edges(n, data=True)), reverse=True)[:5]
    size_map = {n: s for n, s in zip(H.nodes(), node_sizes)}
    nx.draw_networkx_nodes(H, layout, nodelist=top5, ax=ax,
        node_color='white', node_size=[size_map[n] + 700 for n in top5], alpha=0.3)

    nx.draw_networkx_nodes(H, layout, ax=ax,
        node_color=node_colors, node_size=node_sizes,
        alpha=0.95, linewidths=2, edgecolors='white')

    nx.draw_networkx_labels(H, layout, ax=ax,
        font_color='white', font_size=11, font_weight='bold')

    nx.draw_networkx_edge_labels(H, layout, edge_labels=edge_labels, ax=ax,
        font_color='#ffdd57', font_size=8,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1a2e', alpha=0.7, edgecolor='none'))

    # legend
    patches = [mpatches.Patch(color=c, label=t) for t, c in POS_COLORS.items() if t in H.nodes()]
    ax.legend(handles=patches, loc='lower left',
        facecolor='#2c2c54', edgecolor='white',
        labelcolor='white', fontsize=9, title='POS State', title_fontsize=10)

    ax.text(0.01, 0.97, '○ double border = top 5 most active states',
        transform=ax.transAxes, color='#aaaacc', fontsize=8, va='top')
    ax.text(0.01, 0.94, 'edge numbers = transition count',
        transform=ax.transAxes, color='#ffdd57', fontsize=8, va='top')

    ax.set_title(title, color='white', fontsize=15, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('fsm_diagram.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.show()


draw_fsm(G, title='English POS Transition FSM | built from BERT output + corpus')

def get_prob_matrix(G):
    states = sorted(G.nodes())
    idx = {s: i for i, s in enumerate(states)}
    mat = np.zeros((len(states), len(states)))

    for u, v, d in G.edges(data=True):
        mat[idx[u]][idx[v]] = d['weight']

    # normalize each row so probabilities sum to 1
    row_sums = mat.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return mat / row_sums, states


def draw_heatmap(G):
    mat, states = get_prob_matrix(G)

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    im = ax.imshow(mat, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(range(len(states)))
    ax.set_yticks(range(len(states)))
    ax.set_xticklabels(states, rotation=45, ha='right', color='white', fontsize=10)
    ax.set_yticklabels(states, color='white', fontsize=10)

    # label each cell with its probability
    for i in range(len(states)):
        for j in range(len(states)):
            if mat[i][j] > 0:
                color = 'black' if mat[i][j] > 0.4 else 'white'
                ax.text(j, i, f'{mat[i][j]:.2f}', ha='center', va='center', fontsize=8, color=color)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('P(next tag | current tag)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    ax.set_xlabel('Next state', color='white', fontsize=12)
    ax.set_ylabel('Current state', color='white', fontsize=12)
    ax.set_title('Transition Probability Matrix', color='white', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('transition_matrix.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.show()


draw_heatmap(G)

def trace_path(sentence, G):
    pairs = get_pos_tags(sentence)
    tags  = [t for _, t in pairs]
    words = [w for w, _ in pairs]

    print(f'Sentence: "{sentence}"')
    print(f'POS path: {" -> ".join(tags)}')
    print('-' * 55)

    accepted = True
    for i in range(len(tags) - 1):
        src, dst, word = tags[i], tags[i+1], words[i]
        if G.has_edge(src, dst):
            freq = G[src][dst]['weight']
            print(f'  ok  [{src}] --{word}--> [{dst}]  (freq={freq})')
        else:
            print(f'  !!  [{src}] --{word}--> [{dst}]  NOT IN FSM')
            accepted = False

    print()
    print('  ACCEPTED' if accepted else '  REJECTED - unknown transition(s)')


test_sentences = [
    'The dog runs fast.',               # should pass
    'She carefully read the long report.',
    'Colorless green ideas sleep furiously.',  # Chomsky - grammatical but semantically odd
    'Runs dog the fast.',               # ungrammatical - should fail
]

for s in test_sentences:
    trace_path(s, G)
    print('=' * 55)

# change this to whatever you want BERT to fill in
# [MASK] is the keyword that BERT will predict
my_sentence = 'The [MASK] scientist presented her [MASK] findings.'

filled = show_predictions(my_sentence)
trace_path(filled, G)

# add your own sentences to teach the FSM new transitions
extra = [
    'The moon rises above the mountains.',
    'Children play happily in the park.',
    'The government passed a new law.'
]

new_transitions, _ = extract_transitions(extra)
for (u, v), count in new_transitions.items():
    if G.has_edge(u, v):
        G[u][v]['weight'] += count
    else:
        G.add_edge(u, v, weight=count)

print(f'FSM updated: {G.number_of_nodes()} states, {G.number_of_edges()} transitions')
print('Re-run the draw_fsm() cell above to see the updated diagram')
