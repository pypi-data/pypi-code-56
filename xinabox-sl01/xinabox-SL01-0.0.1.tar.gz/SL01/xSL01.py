from xCore import xCore

# Defines VEML6075 Registers
VEML6075_REG_CONF           = 0x00  # Configuration register
VEML6075_REG_UVA            = 0x07  # UVA register
VEML6075_REG_UVB            = 0x09  # UVB register
VEML6075_REG_UVCOMP1        = 0x0A  # Visible compensation register
VEML6075_REG_UVCOMP2        = 0x0B  # IR compensation register

# Defines VEML6075
VEML6075_CONF_HD_NORM       = 0x00  # Normal Dynamic Setting
VEML6075_CONF_HD_HIGH       = 0x80  # High Dynamic Setting
VEML6075_CONF_UV_TRIG_ONCE  = 0x04  # Triggers UV Measurement Once
VEML6075_CONF_UV_TRIG_NORM  = 0x00  # Normal Mode Operation
VEML6075_CONF_AF_FORCE      = 0x00  # Normal Mode Enabled
VEML6075_CONF_AF_AUTO       = 0x02  # Active Force Mode Disabled
VEML6075_CONF_SD_OFF        = 0x00  # Power ON
VEML6075_CONF_SD_ON         = 0x01  # Power OFF

VEML6075_CONF_IT_50         = 0x00  # 50ms
VEML6075_CONF_IT_100        = 0x10  # 100ms
VEML6075_CONF_IT_200        = 0x20  # 200ms
VEML6075_CONF_IT_400        = 0x30  # 400ms
VEML6075_CONF_IT_800        = 0x40  # 800ms

# Page 15/22 VEML6075 AppNote 84339
# No teflon (open air)
VEML6075_UVA_VIS_COEFF      = 2.22
VEML6075_UVA_IR_COEFF       = 1.33
VEML6075_UVB_VIS_COEFF      = 2.95
VEML6075_UVB_IR_COEFF       = 1.74
VEML6075_UVA_RESP           = (1.0 / 684.46)
VEML6075_UVB_RESP           = (1.0 / 385.95)

# Defines TSL4531 Registers
TSL4531_REG_CONTROL     = 0x00  # Control Register Address
TSL4531_REG_CONF        = 0x01  # Configuration Register Address
TSL4531_REG_DATA_LOW    = 0x04  # ADC low byte
TSL4531_REG_DATA_HIGH   = 0x05  # ADC high byte

# Defines TSL4531
TSL4531_WRITE_CMD       = 0x80  # Command Register. Must write as 1.
TSL4531_CONF_PWR_DOWN   = 0x00  # Power OFF
TSL4531_CONF_ONE_RUN    = 0x02  # Run ONCE then Power OFF
TSL4531_CONF_START      = 0x03  # Power ON

TSL4531_CONF_IT_100     = 0x02  # 100ms
TSL4531_CONF_IT_200     = 0x01  # 200ms
TSL4531_CONF_IT_400     = 0x00  # 400ms

TSL4531_CONF_PSAVE      = 0x08

class xSL01:
    def __init__(self):
        self.i2c = xCore()
        self.addrVE = 0x10
        self.addrTS = 0x29
        self.__UVAintensity = 0.0
        self.__UVBintensity = 0.0
        self.__UVindex = 0.0
        self.__rawUVA = 0
        self.__rawUVB = 0
        self.__UVcomp1 = 0
        self.__UVcomp2 = 0
        self.__LUX = 0.0
        self.initTS()
        self.initVE()

    def initVE(self):
        try:
            self.i2c.write_bytes(self.addrVE, VEML6075_REG_CONF, VEML6075_CONF_IT_100)
            self.i2c.write_bytes(self.addrVE, 0x00)
        except Exception as e:
            print(e)

    def getUVA(self):
        self.GET_VEML()
        return self.__UVAintensity

    def getUVB(self):
        self.GET_VEML()
        return self.__UVBintensity

    def getUVIndex(self):
        self.GET_VEML()
        self.calculateIndex()
        return self.__UVindex

    def GET_VEML(self):
        self.readUVdata()
        self.__UVAintensity = float(self.__rawUVA)
        self.__UVBintensity = float(self.__rawUVB)
        self.__UVAintensity -= (VEML6075_UVA_VIS_COEFF * self.__UVcomp1) - (VEML6075_UVA_IR_COEFF * self.__UVcomp2)
        self.__UVBintensity -= (VEML6075_UVB_VIS_COEFF * self.__UVcomp1) - (VEML6075_UVB_IR_COEFF * self.__UVcomp2)

    def readUVdata(self):
        self.__rawUVA = self.readVEML(VEML6075_REG_UVA)
        self.__rawUVB = self.readVEML(VEML6075_REG_UVB)
        self.__UVcomp1 = self.readVEML(VEML6075_REG_UVCOMP1)
        self.__UVcomp2 = self.readVEML(VEML6075_REG_UVCOMP2)

    def calculateIndex(self):
        UVAComp = 0
        UVBComp = 0
        UVAComp = (self.__UVAintensity * VEML6075_UVA_RESP)
        UVBComp = (self.__UVBintensity * VEML6075_UVB_RESP)
        self.__UVindex = (UVAComp + UVBComp)/2.0

    def readVEML(self, reg):
        raw=self.i2c.write_read(self.addrVE, reg, 2)
        value = raw[1]*256 + raw[0]
        return value

    def initTS(self):
        try:
            self.i2c.write_bytes(self.addrTS, (TSL4531_WRITE_CMD | TSL4531_REG_CONTROL), TSL4531_CONF_START)
            self.i2c.write_bytes(self.addrTS, (TSL4531_WRITE_CMD | TSL4531_REG_CONF), TSL4531_CONF_IT_100)
        except Exception as e:
            print(e)

    def getLUX(self):
        self.GET_TSL()
        return self.__LUX

    def GET_TSL(self):
        multi = int(4)
        raw_LUX_H = self.i2c.write_read(self.addrTS, (TSL4531_WRITE_CMD | TSL4531_REG_DATA_HIGH), 1)[0]
        raw_LUX_L = self.i2c.write_read(self.addrTS, (TSL4531_WRITE_CMD | TSL4531_REG_DATA_LOW), 1)[0]
        data = ((raw_LUX_H << 8)|(raw_LUX_L))
        self.__LUX = multi*data