"""
Integration Tests - CLI + Calculator Working Together
"""

import subprocess
import sys
import pytest
import os


class TestCLIIntegration:
    """Test CLI application integrating with
    calculator module"""

    def run_cli(self, *args):
        """Helper method to run CLI and capture output"""
        import os
        import sys
        import subprocess

        # 1. Find the absolute path of this specific test file
        test_file_path = os.path.abspath(__file__) # targets 'tests/integration/test_cli_integration.py'
        
        # 2. Go up two levels to find the true project root directory
        integration_dir = os.path.dirname(test_file_path) # 'tests/integration'
        tests_dir = os.path.dirname(integration_dir)       # 'tests'
        project_root = os.path.dirname(tests_dir)          # 'my-calculator' root folder
        
        # 3. Copy and set up the environment
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root
            
        cmd = [sys.executable, "-m", "src.cli"] + list(args)
        
        # 4. Explicitly run the command from the true project root directory
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root, env=env)
        return result
        

    def test_cli_add_integration(self):
        """Test CLI can perform addition"""
        result = self.run_cli("add", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "8"

    def test_cli_subtract_integration(self):
        """Test CLI can perform subtraction"""
        result = self.run_cli("subtract", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "2"

    def test_cli_subtract_missing_operand_error(self):
        """Test CLI handles missing operand for
        subtraction gracefully"""
        # call subtract with only one operand; CLI should exit with non-zero and print an error
        result = self.run_cli("subtract", "5")
        assert result.returncode == 1
        # CLI prints a generic unexpected error message for this case
        assert result.stdout.strip().startswith("Unexpected error:")

    def test_cli_multiply_integration(self):
        """Test CLI can perform multiplication"""
        result = self.run_cli("multiply", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "15"

    def test_cli_divide_integration(self):
        """Test CLI can perform division"""
        result = self.run_cli("divide", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.67"
