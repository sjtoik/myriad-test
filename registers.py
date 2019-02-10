import json
import enum
import SoapySDR
import collections

from pyLMS7002Soapy import pyLMS7002Soapy


def print_low_level(sdr):
    reg_banks = sdr.LMS7002.regDesc.getRegBanks()
    for bank in reg_banks:
        for register in bank.registers:
            print(f'{bank.name}: {register.name}')


def get_info(sdr):
    """ pyLMS.sdr Soapy driver documentation:
    https://pothosware.github.io/SoapySDR/doxygen/latest/classSoapySDR_1_1Device.html """


class Direction(int, enum.Enum):
    TX = SoapySDR.SOAPY_SDR_TX
    RX = SoapySDR.SOAPY_SDR_RX


if __name__ == '__main__':

    pyLMS = pyLMS7002Soapy.pyLMS7002Soapy(verbose=True)
    banks = pyLMS.LMS7002.getRegisterBanks()

    for bank in banks:
        print(bank)

    info = {
        'clock_sources': pyLMS.sdr.listClockSources(),
        'GPIO_banks': pyLMS.sdr.listGPIOBanks(),
        'register_interfaces': pyLMS.sdr.listRegisterInterfaces(),
        'time_sources': pyLMS.sdr.listTimeSources(),
        'sensors': pyLMS.sdr.listSensors(),
        'UARTs': pyLMS.sdr.listUARTs(),
    }

    for direction in Direction:
        channel_count = pyLMS.sdr.getNumChannels(direction.value)
        info[direction.name] = {}

        for channel in range(channel_count):
            info[direction.name][channel] = {
                'tunable_elements': pyLMS.sdr.listFrequencies(direction, channel),
                'sample_rates': pyLMS.sdr.listSampleRates(direction, channel),
                'gains': pyLMS.sdr.listGains(direction, channel),
                'frequencies': pyLMS.sdr.listFrequencies(direction, channel),
                'bandwidths': pyLMS.sdr.listBandwidths(direction, channel),
                'antennas': pyLMS.sdr.listAntennas(direction, channel),
            }

    print(json.dumps(info, indent=4))
