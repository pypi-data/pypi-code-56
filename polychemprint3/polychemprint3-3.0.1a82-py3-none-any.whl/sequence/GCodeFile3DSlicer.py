# -*- coding: utf-8 -*-
"""
Parameterized code for reading in a gcode file and reprocessing for PCP3

| First created on 05/14/2020 18:16:00
| Revised:
| Author: Bijal Patel

"""
from datetime import datetime

from polychemprint3.axes import axes3DSpec
from polychemprint3.tools.toolSpec import toolSpec
from polychemprint3.sequence.sequenceSpec import sequenceSpec, seqParam
from polychemprint3.tools.nullTool import nullTool
from polychemprint3.axes.nullAxes import nullAxes
import logging

BROKEN
class GCodeFile3DSlicer(sequenceSpec):
    """Sequence template for importing GCODE motion commands and tool triggers into PCP Recipe framework"""

    ################### Construct/Destruct METHODS ###########################
    def __init__(self, axes: axes3DSpec = nullAxes(), tool: toolSpec = nullTool(), **kwargs):
        """*Initializes GCodeFile object with parameters for this sequence*.

        Parameters
        ----------
        axes: axes3DSpec
        tool: toolSpec
        """
        # Get current Date

        dateStr = str(datetime.date(datetime.now()))
        currentDate = dateStr[-5:-3] + '\\' + dateStr[-2:] + '\\' + dateStr[:4]

        # Create Params dict
        self.dictParams = {
            "name": seqParam("name", "GCodeFile3DSlicer", "",
                             "Change if modifying from default"),
            "description": seqParam("Sequence Description",
                                    "Imported from GCodeFile", "", ""),
            "creationDate": seqParam("Creation Date",
                                     currentDate, "", "dd/mm/yyyy"),
            "createdBy": seqParam("Created By", "Bijal Patel", "", ""),
            "owner": seqParam("Owner", "PCP_CoreUtilities", "", "default: PCP_Core"),
            "filePath": seqParam("GCodeFilePath", "PathUnset", "",
                                 "Full File Path to target GCode File"),
            "feedRate": seqParam("Printing Speed", "Default", "mm/min",
                                 "Leave as \"Default\" to use the feedrates from the original GCode file"),
            "trvRate": seqParam("Travel Speed", "Default", "mm/min",
                                "Leave as \"Default\" to use the travel speed from the original GCode file"),
            "Zhop": seqParam("Z hop height", "Default", "mm",
                             "Leave as default to use the original GCode Z-hop height (within layers)"),
            "Ton": seqParam("Tool on Value", "5", "",
                            "Tool value when dispensing"),
            "Toff": seqParam("Tool off Value", "5", "",
                             "Tool value when not dispensing"),
            "Ttrv": seqParam("Tool travel Value", "5", "",
                             "Tool value during travel moves"),
        }

        # Pass values to parent
        super().__init__(axes, tool, self.dictParams, **kwargs)
    ################### Unique Methods  ####################################


    ################### Sequence Methods ###################################
    def genSequence(self):
        """*Loads print sequence into a list into cmdList attribute*.

        Returns
        -------
        bool
            whether successfully reached the end or not
        """
        self.cmdList = []
        cmds = self.cmdList
        try:

            # Pull values for brevity
            feedRate = self.dictParams.get("feedRate").value
            xMove = self.dictParams.get("xMove").value
            yMove = self.dictParams.get("yMove").value
            zMove = self.dictParams.get("zMove").value

            # Step by Step appending commands to list for execution

            # 0 Set positioning mode
            cmds.append("axes.setPosMode(" +  + ")")

            # 1 Move at feed rate in X Y and Z
            cmds.append(("axes.move(\"G1 F" + str(feedRate)
                         + " X" + str(xMove)
                         + " Y" + str(yMove)
                         + " Z" + str(zMove)
                         + "\\n" + "\")"))

            return True

        except KeyboardInterrupt:
            print("\tgenSequence Terminated by User....")
            return False
        except Exception as inst:
            print("\tTerminated by Error....")
            logging.exception(inst)
            return False

    ####################### Logging METHODS ###############################

    def writeLogSelf(self):
        """*Generates log string containing dict to be written to log file*.

        Returns
        -------
        String
            log in string format
        """
        return super().writeLogSelf()

    def loadLogSelf(self, logString):
        """*loads log back into dict*.

        Parameters
        ----------
        logString: String
            log string to be loaded back in

        """
        super().loadLogSelf(logString)
