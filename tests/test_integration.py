import nose
# import custom RFCx modules from modules folder
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules                import service_layer
from modules.domain_modules import load_sound
from modules.domain_modules import spectral_analysis
from modules.domain_modules import sound_profiling
from modules.domain_modules import alerts

# def test_load_sound_module_takes_in_wav_file(self):
#     self.fail()

# def test_load_sound_module_module_puts_out_Sound_obj(self):
#     self.fail()

# def test_spect_analysis_module_takes_in_Sound_obj(self):
#     self.fail()

# def test_spect_analysis_module_puts_out_Spectrum_obj(self):
#     self.fail()

# def test_fingerprinting_module_takes_in_Spectrum_obj(self):
#     self.fail()

# def test_fingerprinting_module_puts_out_Profile_obj(self):
#     self.fail()

# def test_sound_profiling_module_takes_in_Profile_obj(self):
#     self.fail()

# def test_sound_profiling_module_puts_out_Profile_obj(self):
#     self.fail()

# def test_alert_module_takes_in_Profile_obj(self):
#     self.fail()

# def test_alert_module_puts_out_bool_status(self):
#     self.fail()
