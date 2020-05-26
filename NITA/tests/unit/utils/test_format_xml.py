from mock import patch
from mock import MagicMock

import unittest2 as unittest
import unittest
import builtins

from lxml import etree

from jnpr.toby.utils.format_xml import normalize_xml

class TestFormatXMLBasic(unittest.TestCase):
    '''
    Unit test class for Format XML to cover basic tests
    '''

    MX2010_CHASSIS_INFO_XML = '''
        <chassis-inventory>
            <chassis>
                <name>Chassis</name>
                <serial-number>JN1259A3FAFK</serial-number>
                <description>MX2010</description>
                <chassis-module>
                    <name>Midplane</name>
                    <version>REV 47</version>
                    <part-number>750-044636</part-number>
                    <serial-number>ABAD1621</serial-number>
                    <description>Lower Backplane</description>
                    <clei-code>IPMU810ARB</clei-code>
                    <model-number>CHAS-BP-MX2010-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Midplane 1</name>
                    <version>REV 02</version>
                    <part-number>711-044557</part-number>
                    <serial-number>ABAC3844</serial-number>
                    <description>Upper Backplane</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>PMP</name>
                    <version>REV 01</version>
                    <part-number>711-051406</part-number>
                    <serial-number>ACVD0488</serial-number>
                    <description>Power Midplane</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>FPM Board</name>
                    <version>REV 09</version>
                    <part-number>760-044634</part-number>
                    <serial-number>ABDG8729</serial-number>
                    <description>Front Panel Display</description>
                    <clei-code>IPMYA4EJRA</clei-code>
                    <model-number>MX2010-CRAFT-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 0</name>
                    <version>REV 01</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB32000J3</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAKRKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 1</name>      
                    <version>REV 04</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDD418023N</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAMMKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 2</name>
                    <version>REV 04</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB3290655</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAMMKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 3</name>
                    <version>REV 04</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDD4180291</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAMMKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 4</name>
                    <version>REV 04</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDD41801WV</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAMMKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 5</name>
                    <version>REV 01</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB32000G2</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAKRKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 6</name>
                    <version>REV 01</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB3130056</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAKRKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 7</name>
                    <version>REV 01</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB32000J2</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAKRKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 8</name>
                    <version>REV 04</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDD418026W</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAMMKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PDM 0</name>
                    <version>REV 03</version>
                    <part-number>740-045234</part-number>
                    <serial-number>1EFA3230533</serial-number>
                    <description>DC Power Dist Module</description>
                    <clei-code>IPUPAJSKAA</clei-code>
                    <model-number>MX2000-PDM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PDM 1</name>
                    <version>REV 03</version>
                    <part-number>740-045234</part-number>
                    <serial-number>1EFA3230570</serial-number>
                    <description>DC Power Dist Module</description>
                    <clei-code>IPUPAJSKAA</clei-code>
                    <model-number>MX2000-PDM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Routing Engine 0</name>
                    <version>REV 12</version>
                    <part-number>750-055814</part-number>
                    <serial-number>CALL6691</serial-number>
                    <description>RE-S-2X00x8</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>Routing Engine 1</name>
                    <version>REV 12</version>
                    <part-number>750-055814</part-number>
                    <serial-number>CALV3429</serial-number>
                    <description>RE-S-2X00x8</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>CB 0</name>
                    <version>REV 17</version>
                    <part-number>750-055087</part-number>
                    <serial-number>CALP9482</serial-number>
                    <description>MX2K Enhanced SCB</description>
                    <clei-code>COUCAU8BAA</clei-code>
                    <model-number>REMX2K-X8-64G-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>CB 1</name>
                    <version>REV 17</version>
                    <part-number>750-055087</part-number>
                    <serial-number>CALF1519</serial-number>
                    <description>MX2K Enhanced SCB</description>
                    <clei-code>COUCAU8BAA</clei-code>
                    <model-number>REMX2K-X8-64G-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SPMB 0</name>
                    <version>REV 05</version>
                    <part-number>711-041855</part-number>
                    <serial-number>CALP9352</serial-number>
                    <description>PMB Board</description>
                </chassis-module>
                <chassis-module>
                    <name>SPMB 1</name>
                    <version>REV 05</version>
                    <part-number>711-041855</part-number>
                    <serial-number>CALM6346</serial-number>
                    <description>PMB Board</description>
                </chassis-module>
                <chassis-module>
                    <name>SFB 0</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2849</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 1</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2796</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 2</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2785</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 3</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2813</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 4</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2802</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 5</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2786</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SFB 6</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2775</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>            
                    <name>SFB 7</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2794</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>FPC 1</name>
                    <version>REV 82</version>
                    <part-number>750-044130</part-number>
                    <serial-number>ABDM9803</serial-number>
                    <description>MPC6E 3D</description>
                    <clei-code>IP9IATZDAE</clei-code>
                    <model-number>MX2K-MPC6E</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 12</version>
                        <part-number>711-045719</part-number>
                        <serial-number>ABDN4040</serial-number>
                        <description>RMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 1</name>
                        <version>REV 35</version>
                        <part-number>750-046532</part-number>
                        <serial-number>CAMC3598</serial-number>
                        <description>24X10GE SFPP</description>
                        <clei-code>IP9IATVDAA</clei-code>
                        <model-number>MIC6-10G</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 1</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>24X10GE SFPP</description>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 0</name>
                                <version>REV 01</version>
                                <part-number>740-021309</part-number>
                                <serial-number>A9401FL</serial-number>
                                <description>SFP+-10G-LR</description>
                            </chassis-sub-sub-sub-module>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 1</name>
                                <version>REV 01</version>
                                <part-number>740-021309</part-number>
                                <serial-number>A940036</serial-number>
                                <description>SFP+-10G-LR</description>
                            </chassis-sub-sub-sub-module>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>XLM 0</name>
                        <version>REV 14</version>
                        <part-number>711-046638</part-number>
                        <serial-number>ABDL6698</serial-number>
                        <description>MPC6E XL</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>XLM 1</name>
                        <version>REV 14</version>
                        <part-number>711-046638</part-number>
                        <serial-number>ABDK6518</serial-number>
                        <description>MPC6E XL</description>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 2</name>
                    <version>REV 39</version>
                    <part-number>750-063414</part-number>
                    <serial-number>CAMF5918</serial-number>
                    <description>MPC9E 3D</description>
                    <clei-code>IPUCBN5CAE</clei-code>
                    <model-number>MX2K-MPC9E</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 21</version>
                        <part-number>750-057177</part-number>
                        <serial-number>CALY2917</serial-number>
                        <description>SMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 0</name>
                        <version>REV 14</version>
                        <part-number>750-055992</part-number>
                        <serial-number>CALV1654</serial-number>
                        <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        <clei-code>IPUIBY5MAA</clei-code>
                        <model-number>MIC-MRATE</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 0</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 8</name>
                                <version>REV 01</version>
                                <part-number>740-061405</part-number>
                                <serial-number>1ECQ13110CJ</serial-number>
                                <description>QSFP-100G-SR4-T2</description>
                            </chassis-sub-sub-sub-module>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 9</name>
                                <version>REV 01</version>
                                <part-number>740-058734</part-number>
                                <serial-number>1ACQ13150KJ</serial-number>
                                <description>QSFP-100GBASE-SR4</description>
                            </chassis-sub-sub-sub-module>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 1</name>
                        <version>REV 14</version>
                        <part-number>750-055992</part-number>
                        <serial-number>CALV1474</serial-number>
                        <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        <clei-code>IPUIBY5MAA</clei-code>
                        <model-number>MIC-MRATE</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 1</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 3</name>
                    <version>REV 29</version>
                    <part-number>750-054576</part-number>
                    <serial-number>CAEL7916</serial-number>
                    <description>MPC8E 3D</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 8</name>
                    <version>REV 18</version>
                    <part-number>750-086583</part-number>
                    <serial-number>CAMA1800</serial-number>
                    <description>MPC11E 3D</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 19</version>
                        <part-number>750-072571</part-number>
                        <serial-number>CALX6740</serial-number>
                        <description>FMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 0</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>1A</version>
                            <part-number>740-061408</part-number>
                            <serial-number>1FCQ52310FM</serial-number>
                            <description>QSFP-100G-CWDM4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 1</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 1</name>
                            <version>01</version>
                            <part-number>740-061405</part-number>
                            <serial-number>1ECQ14010V0</serial-number>
                            <description>QSFP-100GBASE-SR4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 2</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>01</version>
                            <part-number>740-067443</part-number>
                            <serial-number>QI0606XC</serial-number>
                            <description>CFP-40G-SR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 4</name>
                            <version>1A</version>
                            <part-number>740-064980</part-number>
                            <serial-number>1FCS7415008</serial-number>
                            <description>QSFP28-100G-AOC-30M</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>   
                    <chassis-sub-module>
                        <name>PIC 3</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>A0</version>
                            <part-number>740-058734</part-number>
                            <serial-number>1ACQ13150P8</serial-number>
                            <description>QSFP-100GBASE-SR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 1</name>
                            <version>A0</version>
                            <part-number>740-058734</part-number>
                            <serial-number>1ACQ13150PP</serial-number>
                            <description>QSFP-100GBASE-SR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 4</name>
                            <version>A1</version>
                            <part-number>740-061411</part-number>
                            <serial-number>1ACS42100PM</serial-number>
                            <description>QSFP28-100G-AOC-10M</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 4</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>A</version>
                            <part-number>740-067442</part-number>
                            <serial-number>1ACP13240EL</serial-number>
                            <description>CFP-40G-SR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 3</name>
                            <version>A0</version>
                            <part-number>740-058734</part-number>
                            <serial-number>1ACQ13150KZ</serial-number>
                            <description>QSFP-100GBASE-SR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 4</name>
                            <version>01</version>
                            <part-number>740-061409</part-number>
                            <serial-number>1GCQA41000K</serial-number>
                            <description>QSFP-100GBASE-LR4-T2</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 5</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>1A</version>
                            <part-number>740-058732</part-number>
                            <serial-number>1FCQA3140KB</serial-number>
                            <description>CFP-100G-LR4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 1</name>
                            <version>01</version>
                            <part-number>740-061002</part-number>
                            <serial-number>1RC4321208D</serial-number>
                            <description>UNKNOWN</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 6</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>A</version>
                            <part-number>740-054053</part-number>
                            <serial-number>XX90MPH</serial-number>
                            <description>QSFP+-4X10G-SR</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 3</name>
                            <version>02</version>
                            <part-number>740-061408</part-number>
                            <serial-number>1HTQ5219H4G</serial-number>
                            <description>QSFP-100G-CWDM4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 7</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>1B</version>
                            <part-number>740-054050</part-number>
                            <serial-number>INGAD0092606</serial-number>
                            <description>QSFP+-4X10G-LR</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 1</name>
                            <version>01</version>
                            <part-number>740-061408</part-number>
                            <serial-number>1G1CQ5A34600W</serial-number>
                            <description>QSFP-100G-CWDM4</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 3</name>
                            <version>01</version>
                            <part-number>740-071175</part-number>
                            <serial-number>1DJQL24010Z</serial-number>
                            <description>QSFP-100GBASE-ER4L</description>
                        </chassis-sub-sub-module>
                        <chassis-sub-sub-module>
                            <name>Xcvr 4</name>
                            <version>1A</version>
                            <part-number>740-058732</part-number>
                            <serial-number>1FCQA3140KR</serial-number>
                            <description>CFP-100G-LR4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>Fan Tray 0</name>
                    <version>REV 06</version>
                    <part-number>760-046960</part-number>
                    <serial-number>ACAY0827</serial-number>
                    <clei-code>IPU&#255;&#255;&#255;&#255;&#255;&#255;&#255;</clei-code>
                    <model-number>&#255;X2000-FANTRAY-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Fan Tray 1</name>
                    <version>REV 01</version>
                    <part-number>760-052467</part-number>
                    <serial-number>ACAY5831</serial-number>
                    <description>172mm FanTray - 6 Fans</description>
                    <clei-code>IPUCBENCAA</clei-code>
                    <model-number>MX2000-FANTRAY-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Fan Tray 2</name>
                    <version>REV 06</version>
                    <part-number>760-046960</part-number>
                    <serial-number>ACAY2203</serial-number>
                    <description>172mm FanTray - 6 Fans</description>
                    <clei-code>IPUCBA5CAA</clei-code>
                    <model-number>MX2000-FANTRAY-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Fan Tray 3</name>
                    <version>REV 06</version>
                    <part-number>760-046960</part-number>
                    <serial-number>ACAY1434</serial-number>
                    <description>172mm FanTray - 6 Fans</description>
                    <clei-code>IPUCBA5CAA</clei-code>
                    <model-number>MX2000-FANTRAY-S</model-number>
                </chassis-module>
            </chassis>
        </chassis-inventory>
    '''

    VMX_CHASSIS_INFO_XML = '''
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.4R2/junos">
            <chassis-inventory xmlns="http://xml.juniper.net/junos/18.4R2/junos-chassis">
                <chassis junos:style="inventory">
                    <name>Chassis</name>
                    <serial-number>VMX3bab</serial-number>
                    <description>MX960</description>
                    <chassis-module>
                        <name>Midplane</name>
                    </chassis-module>
                    <chassis-module>
                        <name>Routing Engine 0</name>
                        <serial-number>f72d13a4-99</serial-number>
                        <description>RE-VMX</description>
                    </chassis-module>
                    <chassis-module>
                        <name>CB 0</name>
                        <description>VMX SCB</description>
                    </chassis-module>
                    <chassis-module>
                        <name>FPC 0</name>
                        <description>Virtual FPC</description>
                        <chassis-sub-module>
                            <name>CPU</name>
                            <version>Rev. 1.0</version>
                            <part-number>RIOT-LITE</part-number>
                            <serial-number>BUILTIN</serial-number>
                        </chassis-sub-module>
                        <chassis-sub-module>
                            <name>MIC 0</name>
                            <description>Virtual 20x 1GE(LAN) SFP</description>
                            <chassis-sub-sub-module>
                                <name>PIC 0</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 10x 1GE(LAN) SFP</description>
                            </chassis-sub-sub-module>
                            <chassis-sub-sub-module>
                                <name>PIC 1</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 10x 1GE(LAN) SFP</description>
                            </chassis-sub-sub-module>
                        </chassis-sub-module>
                        <chassis-sub-module>
                            <name>MIC 1</name>
                            <description>Virtual 4x 10GE(LAN) XFP</description>
                            <chassis-sub-sub-module>
                                <name>PIC 2</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 2x 10GE(LAN) XFP</description>
                            </chassis-sub-sub-module>
                            <chassis-sub-sub-module>
                                <name>PIC 3</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 2x 10GE(LAN) XFP</description>
                            </chassis-sub-sub-module>
                        </chassis-sub-module>
                    </chassis-module>
                </chassis>
            </chassis-inventory>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
    '''

    def test_normalize_xml(self):
        '''
        Unit test for method : format_xml.normalize_xml
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertIsInstance(normalize_xml(self.MX2010_CHASSIS_INFO_XML), etree._Element)
        self.assertIsInstance(normalize_xml(self.VMX_CHASSIS_INFO_XML), etree._Element)

class TestFormatXMLNegative(unittest.TestCase):
    '''
    Unit test class for Format XML to cover negative tests
    '''

    VMX_CHASSIS_INFO_XML = '''
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.4R2/junos">
            <chassis-inventory xmlns="http://xml.juniper.net/junos/18.4R2/junos-chassis">
                <chassis junos:style="inventory">
                    <name>Chassis</name>
                    <serial-number>VMX3bab</serial-number>
                    <description>MX960</description>
                    <chassis-module>
                        <name>Midplane</name>
                    </chassis-module>
                    <chassis-module>
                        <name>Routing Engine 0</name>
                        <serial-number>f72d13a4-99</serial-number>
                        <description>RE-VMX</description>
                    </chassis-module>
                    <chassis-module>
                        <name>CB 0</name>
                        <description>VMX SCB</description>
                    </chassis-module>
                    <chassis-module>
                        <name>FPC 0</name>
                        <description>Virtual FPC</description>
                        <chassis-sub-module>
                            <name>CPU</name>
                            <version>Rev. 1.0</version>
                            <part-number>RIOT-LITE</part-number>
                            <serial-number>BUILTIN</serial-number>
                        </chassis-sub-module>
                        <chassis-sub-module>
                            <name>MIC 0</name>
                            <description>Virtual 20x 1GE(LAN) SFP</description>
                            <chassis-sub-sub-module>
                                <name>PIC 0</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 10x 1GE(LAN) SFP</description>
                            </chassis-sub-sub-module>
                            <chassis-sub-sub-module>
                                <name>PIC 1</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 10x 1GE(LAN) SFP</description>
                            </chassis-sub-sub-module>
                        </chassis-sub-module>
                        <chassis-sub-module>
                            <name>MIC 1</name>
                            <description>Virtual 4x 10GE(LAN) XFP</description>
                            <chassis-sub-sub-module>
                                <name>PIC 2</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 2x 10GE(LAN) XFP</description>
                            </chassis-sub-sub-module>
                            <chassis-sub-sub-module>
                                <name>PIC 3</name>
                                <part-number>BUILTIN</part-number>
                                <serial-number>BUILTIN</serial-number>
                                <description>Virtual 2x 10GE(LAN) XFP</description>
                            </chassis-sub-sub-module>
                        </chassis-sub-module>
                    </chassis-module>
                </chassis>
            </chassis-inventory>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
    '''

    @patch('jnpr.toby.utils.format_xml.etree.parse')

    def test_normalize_xml_error(self, parse_mock):
        '''
        Unit test for method : format_xml.normalize_xml to cover OSError
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        parse_mock.side_effect = OSError

        with self.assertRaises(SystemExit):
            normalize_xml(self.VMX_CHASSIS_INFO_XML)

    @patch('jnpr.toby.utils.format_xml.etree.parse')

    def test_normalize_xml_syntax_error(self, parse_mock):
        '''
        Unit test for method : format_xml.normalize_xml to cover XMLSyntaxError
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        parse_mock.side_effect = etree.XMLSyntaxError("Error Message", 0, 0, 0)

        with self.assertRaises(SystemExit):
            normalize_xml(self.VMX_CHASSIS_INFO_XML)

    def test_normalize_xml_text_error(self):
        '''
        Unit test for method : format_xml.normalize_xml to cover incorrect input text
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertFalse(normalize_xml("Content Error"))

if __name__ == '__main__':
    unittest.main()
