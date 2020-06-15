#
# Force load all message types as they are dynamically accessed by message map loader
#
from journey11.src.main.kpubsubai.pb_uniqueworkref_pb2 import PBUniqueWorkRef
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.kpubsubai.pb_state_pb2 import PBState
from journey11.src.lib.state import State
from journey11.src.main.kpubsubai.pb_simplecapability_pb2 import PBSimpleCapability
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.main.kpubsubai.pb_simplesrcsinkproxy_pb2 import PBSimpleSrcSinkProxy
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy
from journey11.src.main.kpubsubai.pb_simplesrcsinkping_pb2 import PBSimpleSrcSinkPing
from journey11.src.main.simple.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.main.kpubsubai.pb_simplesrcsinkpingnotification_pb2 import PBSimpleSrcSinkPingNotification
from journey11.src.main.simple.simplesrcsinkpingnotification import SimpleSrcSinkPingNotification

# todo - need to get this from the RUN Spec.
MSG_MAP_URL = "https://raw.githubusercontent.com/parrisma/AI-Intuition/kafka/journey11/src/main/kpubsubai/message-map.yml"
