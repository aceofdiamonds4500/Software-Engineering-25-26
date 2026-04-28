import tkinter as tk
from tkinter import ttk

import sys
import os

#Imported to handle unique values
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
from config import TrainingConfig

class DataHandlerGUI(tk.Tk):

    def init_data_page(self, class_types):

        class_options = ttk.Combobox(self, values=class_types)
        class_options.pack(side="top", anchor="nw", pady=10, padx=10)

    def __init__(self):
        super().__init__()
        self.title("Medical Training Data Handler")
        self.geometry("600x500")
        self.init_data_page([' Allergy / Immunology', ' Bariatrics',
    ' Cardiovascular / Pulmonary',                     ' Neurology',
                     ' Dentistry',                       ' Urology',
              ' General Medicine',                       ' Surgery',
             ' Speech - Language', ' SOAP / Chart / Progress Notes',
                ' Sleep Medicine',                  ' Rheumatology',
                     ' Radiology',       ' Psychiatry / Psychology',
                      ' Podiatry',     ' Physical Medicine - Rehab',
         ' Pediatrics - Neonatal',               ' Pain Management',
                    ' Orthopedic',                 ' Ophthalmology',
                  ' Office Notes',       ' Obstetrics / Gynecology',
                  ' Neurosurgery',                    ' Nephrology',
                       ' Letters',      ' Lab Medicine - Pathology',
        ' IME-QME-Work Comp etc.',     ' Hospice - Palliative Care',
         ' Hematology - Oncology',              ' Gastroenterology',
          ' ENT - Otolaryngology',                 ' Endocrinology',
        ' Emergency Room Reports',             ' Discharge Summary',
          ' Diets and Nutritions',                   ' Dermatology',
    ' Cosmetic / Plastic Surgery',    ' Consult - History and Phy.',
                  ' Chiropractic',                       ' Autopsy'])
        
if __name__ == "__main__":
    config = TrainingConfig()
    df = pd.read_csv(config.DATA_PATH)
    class_types = df.medical_specialty.unique()
    print(class_types)
    app = DataHandlerGUI()
    app.mainloop()