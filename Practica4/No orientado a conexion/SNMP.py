from pysnmp.hlapi import *

comunidad = "Practica4Virtual"
host = "192.168.100.32"

def getSNMP(OID):
    errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
            CommunityData(comunidad),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(OID))))

    if errorIndication:
        resultado = errorIndication 
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB

    print("\nGet SNMP")
    print(resultado)

getSNMP("1.3.6.1.2.1.1.1.0")
getSNMP("1.3.6.1.2.1.1.4.0")
getSNMP("1.3.6.1.2.1.1.6.0")