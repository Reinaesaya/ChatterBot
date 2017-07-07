from .input_adapter import InputAdapter
from .microsoft import Microsoft
from .gitter import Gitter
from .hipchat import HipChat
from .mailgun import Mailgun
from .terminal import TerminalAdapter
from .variable_input_type_adapter import VariableInputTypeAdapter, TatoraVariableInputTypeAdapter
from .voice_adapter import SimpleVoiceAdapter, TatoraVoiceAdapter


__all__ = (
    'InputAdapter',
    'Microsoft',
    'Gitter',
    'HipChat',
    'Mailgun',
    'TerminalAdapter',
    'VariableInputTypeAdapter', 'TatoraVariableInputTypeAdapter',
    'SimpleVoiceAdapter', 'TatoraVoiceAdapter',
)
