import enum
import SoapySDR

from pyLMS7002Soapy import pyLMS7002Soapy


def print_low_level(sdr):
    reg_banks = sdr.LMS7002.regDesc.getRegBanks()
    for bank in reg_banks:
        for register in bank.registers:
            print(f'{bank.name}: {register.name}')


def get_soapy_info(pyLMS):
    """ pyLMS.sdr Soapy driver documentation:
    https://pothosware.github.io/SoapySDR/doxygen/latest/classSoapySDR_1_1Device.html """
    info = {
        'clock_sources': pyLMS.sdr.listClockSources(),
        'GPIO_banks': pyLMS.sdr.listGPIOBanks(),
        'register_interfaces': pyLMS.sdr.listRegisterInterfaces(),
        'time_sources': pyLMS.sdr.listTimeSources(),
        'sensors': {},
        'UARTs': pyLMS.sdr.listUARTs(),
    }

    for sensor in pyLMS.sdr.listSensors():
        info['sensors'][sensor] = pyLMS.sdr.readSensor(sensor)

    for direction in Direction:
        channel_count = pyLMS.sdr.getNumChannels(direction.value)
        info[direction.name] = {}

        for channel in range(channel_count):
            info[direction.name][channel] = {
                'sample_rates': pyLMS.sdr.listSampleRates(direction, channel),
                'gains': {},
                'gain_ranges': {},
                'gain_is_auto': pyLMS.sdr.getGainMode(direction, channel),
                'frequencies': {},
                'bandwidths': pyLMS.sdr.listBandwidths(direction, channel),
                'available_antennas': pyLMS.sdr.listAntennas(direction, channel),
                'selected_antenna': pyLMS.sdr.getAntenna(direction, channel),
            }

            for gain in pyLMS.sdr.listGains(direction, channel):
                info[direction.name][channel]['gains'][gain] = pyLMS.sdr.getGain(direction, channel, gain)
                grange = pyLMS.sdr.getGainRange(direction, channel, gain)
                info[direction.name][channel]['gain_ranges'][gain] = (grange.minimum(), grange.maximum())

            for element in pyLMS.sdr.listFrequencies(direction, channel):
                info[direction.name][channel]['frequencies'][element] = pyLMS.sdr.getFrequency(direction, channel, element)

    return info


class Direction(int, enum.Enum):
    TX = SoapySDR.SOAPY_SDR_TX
    RX = SoapySDR.SOAPY_SDR_RX


if __name__ == '__main__':

    pyLMS = pyLMS7002Soapy.pyLMS7002Soapy(verbose=True)
    banks = pyLMS.LMS7002.getRegisterBanks()

    for bank in banks:
        print(bank)

    print(f'LRST_RX_A: {pyLMS.LMS7002.CHIP.LRST_RX_A}')

