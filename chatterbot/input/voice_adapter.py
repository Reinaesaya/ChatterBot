from __future__ import unicode_literals
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from chatterbot.utils import input_function
from chatterbot.microphone import *
from chatterbot.constants import *


class SimpleVoiceAdapter(InputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_input(self, audio_timeout=RECV_AUDIO_TIMEOUT):
        """
        Listen for user voice
        """
        rs = openReceiveSocket(host=RECEIVE_AUDIO_HOST, port=RECEIVE_AUDIO_PORT)

        try:
            ms = connectMicrophoneSocket(host=SEND_LISTENCOMMAND_HOST, port=SEND_LISTENCOMMAND_PORT)
            try:
                sendListenCommand(ms, audio_timeout)
            except Exception as e:
                print("Here: "+e)
                pass
            finally:
                ms.close()

            message = str(getMessage(rs))
            print("You: "+message)
        except Exception as e:
            print("Here1: "+e)  
            pass
        finally:
            rs.shutdown(socket.SHUT_RDWR)
            rs.close()

        message = self.processMessage(message)
        return Statement(message)

    def processMessage(self, message):
        """
        Adaptable
        """
        return message



class TatoraVoiceAdapter(SimpleVoiceAdapter):

    def __init__(self, **kwargs):
        super(TatoraVoiceAdapter, self).__init__(**kwargs)
        self.abstractadaptertype = "TATORA"

    def processMessage(self, message):
        if message.startswith('*') and message.endswith('*'):
            if self.control:
                return "--genconvoimage"
            else:
                return "--lookatscreenforconvo"
        else:
            return message