import board
import visualizeBoard
import bezier
import numpy as np
import random
import math


def Bezier(controlPoints,samples):
    middlePositionList = []
    for index in range(len(controlPoints) - 1):
        middlePositionList.append(
            ((controlPoints[index][0] + controlPoints[index + 1][0]) / 2,
             (controlPoints[index][1] + controlPoints[index + 1][1]) / 2))
    middlePositionList.insert(0, middlePositionList[len(middlePositionList) - 1])
    # print(middlePositionList)
    curveX = []
    curveY = []
    for index in range(len(middlePositionList) - 2):
        xPos = []
        yPos = []
        xPos.append(controlPoints[index][0])
        yPos.append(controlPoints[index][1])
        deltaX = controlPoints[index][0] - (middlePositionList[index][0] + middlePositionList[index + 1][0]) / 2
        deltaY = controlPoints[index][1] - (middlePositionList[index][1] + middlePositionList[index + 1][1]) / 2
        xPos.append(middlePositionList[index + 1][0] + deltaX)
        yPos.append(middlePositionList[index + 1][1] + deltaY)
        deltaX = controlPoints[index + 1][0] - (
                    middlePositionList[index + 1][0] + middlePositionList[index + 2][0]) / 2
        deltaY = controlPoints[index + 1][1] - (
                    middlePositionList[index + 1][1] + middlePositionList[index + 2][1]) / 2
        xPos.append(middlePositionList[index + 1][0] + deltaX)
        yPos.append(middlePositionList[index + 1][1] + deltaY)
        xPos.append(controlPoints[index + 1][0])
        yPos.append(controlPoints[index + 1][1])
        curPoints = np.asfortranarray([xPos, yPos])
        curve = bezier.Curve(curPoints, 3)
        sVals = np.linspace(0.0, 1.0, samples)
        data = curve.evaluate_multi(sVals)
        # print("----------------")
        # print(data)
        curveX.extend(data[0])
        curveY.extend(data[1])
    return np.array([curveX, curveY])


def generateTrace(wd, distance_deviation, angle_deviation, samples, show_graph = False):
    # wd for the target word, deviation for the bias from standard trace (if set as 0, the trace is a standard one)
    # distance_deviation will determine the sigma of the normal distribution.
    # The bigger it is, the more it is away from standard (in a large data scale) (supposed to be negative)
    # angle_deviation determine the angle bias from standard trace
    # 在具体设计时，为了让标准差的意义更明确，两点距离将会根据标准距离按照正态随机等比例缩小，
    # 角度的变化量乘上了pi，这意味着角度和距离的标准差都应在【0，1】间为宜（实际使用应为相当小的正，轨迹更贴近用户行为）
    # samples 是相邻两个控制点间采样点的个数
    # set show_graph as True to view the trace on KeyBoard
    wd = wd.upper()
    wdPositionList = []
    angleList = []
    distanceList = []
    for index,ch in enumerate(wd):
        if index > 0:
            if wd[index-1] == ch:
                continue
        wdPositionList.append(board.getCharacterPos(ch))
        if index > 0:
            distance = math.sqrt(pow((wdPositionList[-1][0]-wdPositionList[-2][0]), 2) +
                                 pow((wdPositionList[-1][1]-wdPositionList[-2][1]), 2))
            distanceList.append(distance)
            angle = math.acos((wdPositionList[-1][0]-wdPositionList[-2][0])/distance)
            if wdPositionList[-1][1]-wdPositionList[-2][1] < 0:
                angle = -angle
            angleList.append(angle)
    if len(wdPositionList) == 1:
        if show_graph:
            visualizeBoard.paintPointOnBoard(wdPositionList[0][0],wdPositionList[0][1])
        return np.array([[wdPositionList[0][0]],[wdPositionList[0][1]]])

    wdPositionListBias = [(0, 0)]
    wdPositionListBias[0] = wdPositionList[0]
    for index in range(len(wdPositionList)-1):
        xBias = - abs(random.normalvariate(0, distance_deviation))
        distanceBiased = distanceList[index] + distanceList[index]*xBias
        angleBiased = angleList[index] + random.normalvariate(0, angle_deviation) * math.pi
        wdPositionListBias.append((wdPositionList[index][0] + distanceBiased*math.cos(angleBiased),
                                   wdPositionList[index][1] + distanceBiased*math.sin(angleBiased)))
    wdPositionListBias.append(wdPositionListBias[0])
    trace = Bezier(wdPositionListBias, samples)
    if show_graph:
        visualizeBoard.paintCurveOnBoard(trace[0], trace[1])
    return trace







