from numpy import zeros

from SignalIntegrity.SParameters import File
from SignalIntegrity.SubCircuits import SubCircuit
from SignalIntegrity.Devices import Open
from SignalIntegrity.Devices import Ground
from SignalIntegrity.Devices import Thru
from SignalIntegrity.Devices import SeriesZ
from SignalIntegrity.Devices import TerminationZ
from SignalIntegrity.Devices import ShuntZ
from SignalIntegrity.Devices import Tee
from SignalIntegrity.Devices import MixedModeConverter
from SignalIntegrity.Devices import MixedModeConverterVoltage
from SignalIntegrity.Devices import IdealTransformer
from SignalIntegrity.Devices import CurrentControlledCurrentSource
from SignalIntegrity.Devices import VoltageControlledVoltageSource
from SignalIntegrity.Devices import CurrentControlledVoltageSource
from SignalIntegrity.Devices import VoltageControlledCurrentSource
from SignalIntegrity.Devices import VoltageAmplifier
from SignalIntegrity.Devices import CurrentAmplifier
from SignalIntegrity.Devices import TransresistanceAmplifier
from SignalIntegrity.Devices import TransconductanceAmplifier
from SignalIntegrity.SParameters.Devices import SeriesC
from SignalIntegrity.SParameters.Devices import SeriesL
from SignalIntegrity.SParameters.Devices import TerminationC
from SignalIntegrity.SParameters.Devices import TerminationL
from SignalIntegrity.SParameters.Devices import Mutual
from SignalIntegrity.SParameters.Devices import TLine

class DeviceParser():
    def __init__(self,f,ports,argsList):
        self.m_f=f
        self.m_sp=None
        self.m_spf=None
        if argsList is None:
            return
        if len(argsList) == 0:
            return
        if argsList[0] == 'subcircuit':
            self.m_spf=SubCircuit(self.m_f,argsList[1],
            ' '.join([x if len(x.split())==1 else "\'"+x+"\'" for x in argsList[2:]]))
            return
        argsList=' '.join(argsList).split()
        if argsList[0] == 'file':
            self.m_spf=File(argsList[1]).Resample(self.m_f)
            return
        elif argsList[0] == 'C':
            if ports == 1:
                self.m_spf=TerminationC(self.m_f,float(argsList[1]))
            elif ports == 2:
                self.m_spf=SeriesC(self.m_f,float(argsList[1]))
            return
        elif argsList[0] == 'L':
            if ports == 1:
                self.m_spf=TerminationL(self.m_f,float(argsList[1]))
            elif ports == 2:
                self.m_spf=SeriesL(self.m_f,float(argsList[1]))
            return
        elif argsList[0] == 'R':
            if ports == 1:
                self.m_sp=TerminationZ(float(argsList[1]))
            elif ports == 2:
                self.m_sp=SeriesZ(float(argsList[1]))
            return
        elif argsList[0] == 'Shunt':
            self.m_sp=ShuntZ(ports,float(argsList[1]))
            return
        elif argsList[0] == 'M':
            self.m_sp=Mutual(self.m_f,float(argsList[1]))
            return
        elif argsList[0] == 'ground':
            self.m_sp=Ground()
            return
        elif argsList[0] == 'open':
            self.m_sp=Open()
            return
        elif argsList[0] == 'thru':
            self.m_sp=Thru()
            return
        elif argsList[0] == 'termination':
            self.m_sp=zeros(shape=(ports,ports)).tolist()
            return
        elif argsList[0] == 'tee':
            self.m_sp=Tee(ports)
            return
        elif argsList[0] == 'mixedmode':
            if len(argsList) > 1:
                if argsList[1] == 'voltage':
                    self.m_sp=MixedModeConverterVoltage()
            else:
                self.m_sp=MixedModeConverter()
            return
        elif argsList[0] == 'idealtransformer':
            if len(argsList) > 1:
                self.m_sp=IdealTransformer(float(argsList[1]))
            else:
                self.m_sp=IdealTransformer()
            return
        elif argsList[0] == 'voltagecontrolledvoltagesource':
            self.m_sp=VoltageControlledVoltageSource(float(argsList[1]))
            return
        elif argsList[0] == 'currentcontrolledcurrentsource':
            self.m_sp=CurrentControlledCurrentSource(float(argsList[1]))
            return
        elif argsList[0] == 'currentcontrolledvoltagesource':
            self.m_sp=CurrentControlledVoltageSource(float(argsList[1]))
            return
        elif argsList[0] == 'voltagecontrolledcurrentsource':
            self.m_sp=VoltageControlledCurrentSource(float(argsList[1]))
            return

        # multi argument tag/key functions
        if len(argsList) > 2:
            a = dict([(argsList[i].lower(),float(argsList[i+1])) for i in range(1,len(argsList),2)])

        if argsList[0] == 'voltageamplifier':
            v=dict([('zo',0),('zi',1e8),('z0',50.)]) # defaults
            v.update(a)
            self.m_sp=VoltageAmplifier(ports,v['gain'],v['zi'],v['zo'])
            return
        elif argsList[0] == 'currentamplifier':
            v=dict([('zo',1e8),('zi',0),('z0',50.)]) # defaults
            v.update(a)
            self.m_sp=CurrentAmplifier(ports,v['gain'],v['zi'],v['zo'])
            return
        elif argsList[0] == 'transresistanceamplifier':
            v=dict([('zo',0.),('zi',0.),('z0',50.)]) # defaults
            v.update(a)
            self.m_sp=TransresistanceAmplifier(ports,v['gain'],v['zi'],v['zo'])
            return
        elif argsList[0] == 'transconductanceamplifier':
            v=dict([('zo',1e8),('zi',1e8),('z0',50.)]) # defaults
            v.update(a)
            self.m_sp=TransconductanceAmplifier(ports,v['gain'],v['zi'],v['zo'])
            return
        elif argsList[0] == 'tline':
            v=dict([('zc',50.),('td',0.)]) # defaults
            v.update(a)
            self.m_spf=TLine(self.m_f,ports,v['zc'],v['td'])
            return