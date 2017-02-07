import sys
from datetime import datetime, timedelta
from array import array
from numpy import hsplit, asarray

class ECG:
    '''Checks validity of selected .ecg file. If it is valid .ecg file creates an instance with all the data stored in .ecg file''' 
    def __init__(self, filename, enc='cp1250'):
        '''Default encoding is set to cp1250 - set accordingly to your needs'''
        self.leadNamesDict = {0:'Unknown', 1:'Bipolar', 2:'X biploar', 3:'Y bipolar', 4:'Z biploar', \
            5:'I', 6:'II', 7:'III', 8:'VR', 9:'VL', 10:'VF', \
            11:'V1', 12:'V2', 13:'V3', 14:'V4', 15:'V5', 16:'V6', \
            17:'ES', 18:'AS', 19:'AI'}
        self.fn = filename
        self.enc = enc
        if not self.fn:
            NoneFileSpecified()
        with open(self.fn, mode='rb') as ecgFile:
            self.magicNumber = ecgFile.read(8).decode(self.enc)
            if self.magicNumber != 'ISHNE1.0':
                raise Exception('File does not have \'ISHNE1.0\' string in the first 8 bytes')
            self.crc = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.headerFixedLength = 512
            self.headerVariableLength = int.from_bytes(ecgFile.read(4), byteorder='little', signed=True)
            #get back to 10th byte where header starts
            ecgFile.seek(10)
            self.headerWhole = ecgFile.read(self.headerFixedLength + self.headerVariableLength)
            crc = int(self.compute_crc(self.headerWhole),2)
            if (crc != self.crc):
                raise Exception('CRC check for file failed. Computed CRC: {0}, CRC in file: {1}'.format(crc, self.crc))
            #get back to 14th byte just after headerVariableLength
            ecgFile.seek(14)
            self.channelNumberOfSamples = int.from_bytes(ecgFile.read(4), byteorder='little', signed=True)
            self.headerVariableOffset = int.from_bytes(ecgFile.read(4), byteorder='little', signed=True)
            self.ecgBytesBlockOffset = int.from_bytes(ecgFile.read(4), byteorder='little', signed=True)
            self.fileVersion = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.patientFirstName = ecgFile.read(40).decode(self.enc)
            self.patientFirstName = self.patientFirstName.split('\x00', 1)[0]
            self.patientLastName = ecgFile.read(40).decode(self.enc)
            self.patientLastName = self.patientLastName.split('\x00', 1)[0]
            self.patientID = ecgFile.read(20).decode(self.enc)
            self.patientID = self.patientID.split('\x00', 1)[0]
            self.patientSex = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.patientRace = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            #patient date of birth as [dd,mm,yy]
            dob = list()
            for i in range(0,3):
                dob.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=True))
            self.patientDateOfBirth = datetime(dob[2], dob[1], dob[0])
            # date of test recording as [dd,mm,yy]
            dor = list()
            for i in range(0,3):
                dor.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=True))
            #date of file creation as [dd,mm,yy]
            dof = list()
            for i in range(0,3):
                dof.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=True))
            self.dateOfFileCreation = datetime(dor[2], dor[1], dor[0])
            #testStart - time of test begining HH:MM:SS
            testStart = list()
            for i in range(0,3):
                testStart.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=True))
            self.datetimeStartOfTest = datetime(dor[2],dor[1],dor[0],testStart[0],testStart[1],testStart[2])
            self.numberOfLeads = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.leadsSpecs = list()
            self.leadsNames = list()
            for i in range(0,12):
                spec = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
                self.leadsSpecs.append(spec)
                self.leadsNames.append(self.leadNamesDict[spec])
            self.leadsQuality = list()
            for i in range(0,12):
                self.leadsQuality.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=True))
            self.leadsResolution = list()
            for i in range(0,12):
                self.leadsResolution.append(int.from_bytes(ecgFile.read(2), byteorder='little', signed=False))
            self.pacemaker = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.recorderType = ecgFile.read(40).decode(self.enc)
            self.recorderType = self.recorderType.split('\x00', 1)[0]
            self.samplingRate = int.from_bytes(ecgFile.read(2), byteorder='little', signed=True)
            self.datetimeEndOfTest = self.datetimeStartOfTest + timedelta(seconds=int(self.channelNumberOfSamples/self.samplingRate))
            self.fileProperiaty = ecgFile.read(80).decode(self.enc)
            self.fileProperiaty = self.fileProperiaty.split('\x00', 1)[0]
            self.fileCopyright = ecgFile.read(80).decode(self.enc)
            self.fileCopyright = self.fileCopyright.split('\x00', 1)[0]
            self.reserved = ecgFile.read(80).decode(self.enc)
            self.reserved = self.reserved.split('\x00', 1)[0]
            self.reserved = ecgFile.read(80).decode(self.enc)
            self.reserved = self.reserved.split('\x00', 1)[0]
            self.headerVariable = ecgFile.read(self.headerVariableLength).decode(self.enc)
            if len(self.headerVariable) > 0:
                self.headerVariable = self.headerVariable.split('\x00', 1)[0]
            ecgFile.seek(self.ecgBytesBlockOffset)
            ecgBytes = array('h')
            ecgBytes.fromfile(ecgFile, self.channelNumberOfSamples * self.numberOfLeads)
            ecgBytesArray = asarray(ecgBytes)
            ecgBytesArray = ecgBytesArray.reshape(-1,self.numberOfLeads)
            self.ecgInChannels = hsplit(ecgBytesArray, self.numberOfLeads)
        
    def compute_crc(self, data: bytes):
        rol = lambda val, r_bits, max_bits: \
        (val << r_bits%max_bits) & (2**max_bits-1) | \
        ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
        b = bytearray()
        data = bytearray(data)
        crc=0xFFFF
        crchi, crclo = divmod(crc, 0x100)

        for a in data:        
            a = a ^ crchi
            crchi = a
            a = a >> 4
            a = a ^ crchi
            crchi = crclo
            crclo = a
            a = rol(a,4,8)
            b=a
            a = rol(a,1,8)
            a = a & 0x1F
            crchi = a ^ crchi
            a = b & 0xF0
            crchi = a ^ crchi
            b = rol(b,1,8)
            b = b & 0xE0
            crclo = b ^ crclo
        checksum = bin(crchi) + bin(crclo)
        checksum = checksum[:9] + '0' + checksum[11:]
        return checksum

class NoneFileSpecified(Exception):
    '''Filename can not be empty'''
