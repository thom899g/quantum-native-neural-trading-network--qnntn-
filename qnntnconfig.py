"""
QNNTN Configuration Management
Handles environment variables, Firebase initialization, and trading parameters
"""
import os
import logging
from dataclasses import dataclass
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class QNNTNConfig:
    """Central configuration for QNNTN system"""
    
    # Firebase Configuration
    firebase_credential_path: str = "config/firebase-credentials.json"
    firestore_collection: str = "qnntn_trading_state"
    
    # Trading Parameters
    max_position_size: float = 10000.0  # USD
    max_drawdown_percent: float = 10.0
    confidence_threshold: float = 0.7
    
    # Data Collection
    data_sources: list = None
    default_symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    
    # Neural Network
    hidden_layers: tuple = (128, 64, 32)
    learning_rate: float = 0.001
    dropout_rate: float = 0.3
    
    def __post_init__(self):
        """Initialize with environment variables"""
        if self.data_sources is None:
            self.data_sources = ["ccxt_binance", "ccxt_kraken"]
        
        # Override with environment variables if present
        env_max_size = os.getenv("QNNTN_MAX_POSITION_SIZE")
        if env_max_size:
            self.max_position_size = float(env_max_size)
        
        # Validate critical parameters
        if self.max_position_size <= 0:
            raise ValueError("max_position_size must be positive")
        if not 0 < self.confidence_threshold < 1:
            raise ValueError