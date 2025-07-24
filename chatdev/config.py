# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration management for ChatDev.
    
    This class handles loading configuration from environment variables
    and .env files with proper fallback mechanisms.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            env_file: Path to .env file. If None, will look for .env in current directory.
        """
        # Load .env file if it exists
        if env_file is None:
            env_file = ".env"
        
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"Loaded configuration from {env_file}")
        elif os.path.exists(os.path.join(os.path.dirname(__file__), "..", env_file)):
            # Try to find .env in project root
            env_path = os.path.join(os.path.dirname(__file__), "..", env_file)
            load_dotenv(env_path)
            print(f"Loaded configuration from {env_path}")
        else:
            print("No .env file found, using environment variables only")
    
    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key from environment variables.
        
        Returns:
            OpenAI API key
            
        Raises:
            ValueError: If API key is not found
        """
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment variables."
            )
        return api_key
    
    @property
    def base_url(self) -> Optional[str]:
        """Get base URL for OpenAI-compatible API.
        
        Returns:
            Base URL if set, None otherwise
        """
        return os.environ.get('BASE_URL')
    
    @property
    def default_model(self) -> str:
        """Get default model name.
        
        Returns:
            Default model name
        """
        return os.environ.get('DEFAULT_MODEL', 'GPT_3_5_TURBO')
    
    @property
    def is_custom_api(self) -> bool:
        """Check if using custom API endpoint.
        
        Returns:
            True if using custom API endpoint, False otherwise
        """
        return self.base_url is not None and self.base_url.strip() != ""
    
    @property
    def temperature(self) -> float:
        """Get temperature setting for model.
        
        Returns:
            Temperature value
        """
        try:
            return float(os.environ.get('TEMPERATURE', '0.2'))
        except ValueError:
            return 0.2
    
    @property
    def top_p(self) -> float:
        """Get top_p setting for model.
        
        Returns:
            Top_p value
        """
        try:
            return float(os.environ.get('TOP_P', '1.0'))
        except ValueError:
            return 1.0
    
    @property
    def max_retries(self) -> int:
        """Get maximum number of retries for API calls.
        
        Returns:
            Maximum retries
        """
        try:
            return int(os.environ.get('MAX_RETRIES', '5'))
        except ValueError:
            return 5
    
    def get_model_config(self) -> dict:
        """Get model configuration dictionary.
        
        Returns:
            Dictionary containing model configuration
        """
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": 1,
            "stream": False,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "logit_bias": {},
        }


# Global configuration instance
_config = None


def get_config(env_file: Optional[str] = None) -> Config:
    """Get global configuration instance.
    
    Args:
        env_file: Path to .env file
        
    Returns:
        Configuration instance
    """
    global _config
    if _config is None:
        _config = Config(env_file)
    return _config


def reload_config(env_file: Optional[str] = None) -> Config:
    """Reload configuration from .env file.
    
    Args:
        env_file: Path to .env file
        
    Returns:
        New configuration instance
    """
    global _config
    _config = Config(env_file)
    return _config