package com.example.myapplication.network

import kotlinx.coroutines.Dispatchers
import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.utils.io.*
import kotlinx.coroutines.withContext
import kotlinx.coroutines.*

class Connection(private val host: String, private val port: Int) {

    private val selectorManager = SelectorManager(Dispatchers.IO)
    private var socket: Socket? = null
    private var receiveChannel: ByteReadChannel? = null
    private var sendChannel: ByteWriteChannel? = null

    suspend fun exchangeData(data: String): String {
        return withContext(Dispatchers.IO) {
            try {
                if (socket == null || socket!!.isClosed) {
                    socket = aSocket(selectorManager).tcp().connect(host, port)
                    receiveChannel = socket!!.openReadChannel()
                    sendChannel = socket!!.openWriteChannel(autoFlush = true)
                }

                sendChannel?.writeStringUtf8(data)

                val buffer = ByteArray(1024)
                val bytesRead = receiveChannel?.readAvailable(buffer) ?: 0

                if (bytesRead > 0) {
                    String(buffer, 0, bytesRead, Charsets.UTF_8)
                } else {
                    "Error: No response"
                }
            } catch (e: Exception) {
                socket?.close()
                "Error: ${e.message}"
            }
        }
    }

    fun close() {
        socket?.close()
        selectorManager.close()
    }
}