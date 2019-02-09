import SoapySDR
from pyLMS7002Soapy import LMS7002
from pyLMS7002Soapy.pyLMS7002Soapy import pyLMS7002Soapy


if __name__ == '__main__':
    sdr = pyLMS7002Soapy(0)

    registers = sdr.LMS7002.regDesc.regNameDict
    for key, value in registers.items():
        print(key)

    mSPI_DFM = sdr.LMS7002.regDesc.getRegistersByName(['mSPI_DFM'])
    mSPI_DFM_address = sdr.LMS7002.regDesc.getRegisterAddresesByName(['mSPI_DFM'])
    print('mSPI_DFM:')
    print(mSPI_DFM)
    print('mSPI_DFM_address:')
    print(mSPI_DFM_address)

