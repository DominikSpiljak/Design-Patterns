import tkinter as tk
import tkinter.filedialog
import math
import abc
from abc import abstractmethod, ABC


class Point:

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def getX(self) -> float:
        return self._x

    def getY(self) -> float:
        return self._y

    def translate(self, dp):
        return Point(self.getX() + dp.getX(), self.getY() + dp.getY())

    def difference(self, dp):
        return Point(self.getX() - dp.getX(), self.getY() - dp.getY())


class Stack:
    
    def __init__(self, stack = None):
        if stack is None:
            self._stack = []
        else:
            self._stack = stack
        
    def empty(self) -> bool:
        return not bool(len(self._stack))
    
    def push(self, element) -> None:
        self._stack.append(element)

    def pop(self):
        if self.empty():
            raise ValueError("Trying to pop from empty stack")
        return self._stack.pop()
    

class GraphicObjectListener(ABC):

    @abstractmethod
    def graphicalObjectChanged(self, go) -> None:
        pass

    @abstractmethod
    def graphicalObjectSelectionChanged(self, go) -> None:
        pass


class Renderer(ABC):

    @abstractmethod
    def drawLine(self, s: Point, e: Point) -> None:
        pass

    @abstractmethod
    def fillPolygon(self, points: list) -> None:
        pass


class GeometryUtil:

    @staticmethod
    def distanceFromPoint(point1: Point, point2: Point) -> float:
        return math.sqrt((point1.getX() - point2.getX()) ** 2 + (point1.getY() - point2.getY()) ** 2)

    @staticmethod
    def distanceFromLineSegment(s: Point, e: Point, p: Point) -> float:
        #TODO: FIX distanceFromLineSegment method
        def line(s, e):
            a = (e.getY() - s.getY())/(e.getX() - s.getX())
            b = a * -s.getX() + s.getY()
            return [a, b]
        
        s, e = sorted([s, e], key=lambda point: (point.getX(), point.getY()))

        # If start point and end point are equal, return distance from either one
        if e.getX() == s.getX() and e.getY() == s.getY():
            return GeometryUtil.distanceFromPoint(p, e)

        # Check for edge case where sx - ex = 0
        if e.getX() == s.getX():
            if p.getY() <= s.getY():
                return GeometryUtil.distanceFromPoint(p, s)
            elif p.getY() >= e.getY():
                return GeometryUtil.distanceFromPoint(p, e)
            else:
                if p.getX() == e.getX():
                    return 0.0
                else:
                    return GeometryUtil.distanceFromPoint(p, Point(s.getX(), p.getY()))

        # Check for edge case where sy - ey = 0
        if e.getY() == s.getY():
            if p.getX() <= s.getX():
                return GeometryUtil.distanceFromPoint(p, s)
            elif p.getX() >= e.getX():
                return GeometryUtil.distanceFromPoint(p, e)
            else:
                if p.getY() == e.getY():
                    return 0.0
                else:
                    return GeometryUtil.distanceFromPoint(p, Point(p.getX(), s.getY()))

        a, b = line(s, e)
        # Line is not vertical and point is on the line
        if a * p.getX() + b == p.getY():
            if p.getX() <= s.getX():
                return GeometryUtil.distanceFromPoint(s, p)
            elif p.getX() >= e.getX():
                return GeometryUtil.distanceFromPoint(e, p)
            else:
                return 0.0
        # Line is not vertical and point is not on the line
        else:
            #Find vertical from point to line
            a_v = -1/a
            b_v = p.getY() - a_v * p.getX()
            x = (b - b_v) / (a_v - a)
            y = a_v * x + b_v
            if x <= e.getX() and x >= s.getX():
                return GeometryUtil.distanceFromPoint(p, Point(x, y))
            elif x > e.getX():
                return GeometryUtil.distanceFromPoint(p, e)
            else:
                return GeometryUtil.distanceFromPoint(p, s)


class Rectangle:
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def getX(self) -> float:
        return self._x

    def getY(self) -> float:
        return self._y

    def getWidth(self) -> float:
        return self._width

    def getHeight(self) -> float:
        return self._height


class GraphicalObject:

    def isSelected(self) -> bool:
        pass

    def setSelected(self, selected: bool) -> None:
        pass

    def getNumberOfHotpoints(self) -> int:
        pass

    def getHotPoint(self, index: int) -> Point:
        pass

    def setHotPoint(self, index: int, hotpoint: Point) -> None:
        pass

    def isHotPointSelected(self, index: int) -> None:
        pass

    def setHotPointSelected(self, index: int, selected: bool) -> None:
        pass

    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        pass

    def translate(self, delta: Point) -> None:
        pass
    
    def getBoundingBox(self) -> Rectangle:
        pass

    def selectionDistance(self, mousePoint: Point) -> float:
        pass

    def render(self, r) -> None:
        pass

    def addGraphicalObjectListener(self, listener) -> None:
        pass

    def removeGraphicalObjectListener(self, listener) -> None:
        pass

    def getShapeName(self) -> str:
        pass

    def duplicate(self):
        pass

    def getShapeID(self) -> str:
        pass

    def load(self, stack: Stack, data: str) -> None:
        pass

    def save(self, rows: list):
        pass


class AbstractGraphicalObject(GraphicalObject, ABC):
    _hot_points: list
    _hot_points_selected: list
    _selected: bool
    _listeners: list

    def __init__(self, points: list = None):
        if points:
            self._hot_points = points
            self._hot_points_selected = [False] * len(points)
        else:
            self._hot_points = []
            self._hot_points_selected = []
        self._selected = False
        self._listeners = []

    def getHotPoint(self, index: int) -> Point:
        return self._hot_points[index]
    
    def setHotPoint(self, index: int,  point: Point) -> None:
        self._hot_points[index] = point
        self.notifyListeners()

    def getNumberOfHotpoints(self) -> int:
        return len(self._hot_points)

    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        return GeometryUtil.distanceFromPoint(self.getHotPoint(index), mousePoint)
    
    def isHotPointSelected(self, index: int) -> bool:
        return self._hot_points_selected[index]
    
    def setHotPointSelected(self, index: int, selected: bool) -> None:
        self._hot_points_selected[index] = selected

    def isSelected(self) -> bool:
        return self._selected

    def setSelected(self, selected: bool) -> None:
        self._selected = selected 
        self.notifySelectionListeners()

    def translate(self, point: Point) -> None:
        for i in range(len(self._hot_points)):
            self._hot_points[i] = self._hot_points[i].translate(point)
        self.notifyListeners()
    
    def addGraphicalObjectListener(self, listener) -> None:
        self._listeners.append(listener)

    def removeGraphicalObjectListener(self, listener) -> None:
        self._listeners.remove(listener)

    def notifyListeners(self) -> None:
        for l in self._listeners:
            l.graphicalObjectChanged(self)

    def notifySelectionListeners(self) -> None:
        for l in self._listeners:
            l.graphicalObjectSelectionChanged(self)


class LineSegment(AbstractGraphicalObject):

    def __init__(self, s: Point = None, e: Point = None):
        if s is not None:
            _starting_point = s
        else:
            _starting_point = Point(0, 0)
        
        if e is not None:
            _ending_point = e
        else:
            _ending_point = Point(10, 0)

        super().__init__([_starting_point, _ending_point])

    def selectionDistance(self, mousePoint: Point) -> float:
        return GeometryUtil.distanceFromLineSegment(self.getHotPoint(0), self.getHotPoint(1), mousePoint)

    def getBoundingBox(self) -> Rectangle:
        starting_point, ending_point = sorted(self._hot_points, key=lambda vertex: (vertex.getX(), vertex.getY()))
        width, height = ending_point.difference(starting_point).getX(), ending_point.difference(starting_point).getY()
        return Rectangle(starting_point.getX(), starting_point.getY(), width, height)

    def duplicate(self):
        return LineSegment(self.getHotPoint(0), self.getHotPoint(1))
    
    def getShapeName(self) -> str:
        return "Linija"

    def render(self, renderer) -> None:
        renderer.drawLine(self.getHotPoint(0), self.getHotPoint(1))

    @staticmethod
    def getShapeID():
        return '@LINE'

    def save(self, rows):
        rows.append('{} {} {} {} {}'.format(LineSegment.getShapeID(), self.getHotPoint(0).getX(),
         self.getHotPoint(0).getY(), self.getHotPoint(1).getX(), self.getHotPoint(1).getY()))

    @staticmethod
    def load(stack, data):
        stack.push(LineSegment(Point(float(data[0]), float(data[1])), Point(float(data[2]), float(data[3]))))


class Oval(AbstractGraphicalObject):
    _center: Point

    def __init__(self, r: Point = None, b: Point = None):
        if r is not None:
            _right_hotpoint = r
        else:
            _right_hotpoint = Point(10, 0)
        
        if b is not None:
            _bottom_hotpoint = b
        else:
            _bottom_hotpoint = Point(0, 10)

        super().__init__([_right_hotpoint, _bottom_hotpoint])
        self._center = Point(_bottom_hotpoint.getX(), _right_hotpoint.getY())


    def translate(self, point: Point) -> None:
        super().translate(point)
        self._center = self._center.translate(point)


    def selectionDistance(self, mousePoint: Point) -> float:
        rectangle = self.getBoundingBox()

        #Check if mousePoint is inside object
        rectangle_x_range = sorted([rectangle.getX(), rectangle.getX() + rectangle.getWidth()])
        rectangle_y_range = sorted([rectangle.getY(), rectangle.getY() + rectangle.getHeight()])
        if mousePoint.getX() >= rectangle_x_range[0] and mousePoint.getX() <= rectangle_x_range[1] and\
           mousePoint.getY() >= rectangle_y_range[0] and mousePoint.getY() <= rectangle_y_range[1]:
            return 0
        
        points = []
        points.append(Point(rectangle.getX(), rectangle.getY()))
        points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY()))
        points.append(Point(rectangle.getX(), rectangle.getY() + rectangle.getHeight()))
        points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()))
        line_segments = [(points[0], points[1]),(points[0], points[2]),
                         (points[1], points[3]), (points[2], points[3])]
        return min([GeometryUtil.distanceFromLineSegment(ls[0], ls[1], mousePoint) for ls in line_segments])

    def getBoundingBox(self) -> Rectangle:
        bottom_hotpoint, right_hotpoint = sorted(self._hot_points, key=lambda vertex: (vertex.getX(), vertex.getY()))
        rectangle_point_x = 2 * bottom_hotpoint.getX() - right_hotpoint.getX()
        rectangle_point_y = bottom_hotpoint.getY()
        width = right_hotpoint.getX() - rectangle_point_x
        height = 2 * right_hotpoint.getY() - 2 * bottom_hotpoint.getY()
        return Rectangle(rectangle_point_x, rectangle_point_y, width, height)

    def duplicate(self):
        return Oval(self.getHotPoint(0), self.getHotPoint(1))
    
    def getShapeName(self) -> str:
        return "Oval"

    def render(self, rendrer):
        #Create points
        points = []
        boundingBox = self.getBoundingBox()
        start_x = boundingBox.getX()
        end_x = boundingBox.getX() + boundingBox.getWidth()

        #Get discrete x's
        xes = []
        x = start_x
        while x <= end_x:
            xes.append(x)
            x += .1


        self._center = Point(self.getHotPoint(1).getX(), self.getHotPoint(0).getY())
        
        #Calculate elipse equation

        a = boundingBox.getWidth() / 2
        b = boundingBox.getHeight() / 2
        p = self._center.getX()
        q = self._center.getY()

        for x in xes:
            #TODO: Fix math domain error
            try:
                y1 = math.sqrt((1 - (x - p) ** 2 / a ** 2) * b ** 2) + q
                y2 = - math.sqrt((1 - (x - p) ** 2 / a ** 2) * b ** 2) + q

                if y1 != y2:
                    index = int(len(points)/2)
                    points.insert(index, Point(x, y1))
                    points.insert(index + 1, Point(x, y2))
            except ValueError:
                pass

        rendrer.fillPolygon(points)

    @staticmethod
    def getShapeID():
        return '@OVAL'

    def save(self, rows):
        rows.append('{} {} {} {} {}'.format(Oval.getShapeID(), self.getHotPoint(0).getX(),
         self.getHotPoint(0).getY(), self.getHotPoint(1).getX(), self.getHotPoint(1).getY()))

    @staticmethod
    def load(stack, data):
        stack.push(Oval(Point(float(data[0]), float(data[1])), Point(float(data[2]), float(data[3]))))


class DocumentModelListener(ABC):

    @abstractmethod
    def documentChange(self) -> None:
        pass
    

class DocumentModel:

    class DocumentModelGOListener:

        def __init__(self, notify_method_changed, notify_method_selection_changed):
            self._notify_method_changed = notify_method_changed
            self._notify_method_selection_changed = notify_method_selection_changed

        def graphicalObjectChanged(self, go) -> None:
            self._notify_method_changed(go)

        def graphicalObjectSelectionChanged(self, go) -> None:
            self._notify_method_selection_changed(go)

    _SELECTION_PROXIMITY = 10
    _objects: list
    _roObjects: tuple
    _listeners: list
    _selectedObjects: list
    _roSelectedObjects: tuple
    _goListener: GraphicObjectListener

    def __init__(self):
        self._objects = []
        self._roObjects = tuple(self._objects)
        self._listeners = []
        self._selectedObjects = []
        self._roSelectedObjects = tuple(self._selectedObjects)
        self._goListener = self.DocumentModelGOListener(self._graphicalObjectChanged, self._graphicalObjectSelectionChanged)

    def clear(self) -> None:
        for o in self._objects:
            o.removeGraphicalObjectListener(self._goListener)
        self._objects = []
        self._selectedObjects = []
        self._doBookkeeping()
        self.notifyListeners()

    def _doBookkeeping(self) -> None:
        self._roObjects = tuple(self._objects)
        self._roSelectedObjects = tuple(self._selectedObjects)

    def addGraphicalObject(self, graphical_object: GraphicalObject) -> None:
        graphical_object.addGraphicalObjectListener(self._goListener)
        self._objects.append(graphical_object)
        if graphical_object.isSelected():
            self._selectedObjects.append(graphical_object)
        self._doBookkeeping()
        self.notifyListeners()

    def removeGraphicalObject(self, graphical_object: GraphicalObject) -> None:
        if graphical_object in self._objects:
            graphical_object.removeGraphicalObjectListener(self._goListener)
            self._objects.remove(graphical_object)
            if graphical_object.isSelected():
                self._selectedObjects.remove(graphical_object)
            self._doBookkeeping()
        self.notifyListeners()

    def list(self) -> tuple:
        return self._roObjects

    def addDocumentModelListener(self, listener: DocumentModelListener) -> None:
        self._listeners.append(listener)

    def removeDocumentModelListener(self, listener: DocumentModelListener) -> None:
        self._listeners.remove(listener)

    def _graphicalObjectChanged(self, go: GraphicalObject):
        self.notifyListeners()
    
    def _graphicalObjectSelectionChanged(self, go: GraphicalObject):
        if go.isSelected() and go not in self._selectedObjects:
            self._selectedObjects.append(go)
        elif not go.isSelected() and go in self._selectedObjects:
            self._selectedObjects.remove(go)
        self._doBookkeeping()
        self.notifyListeners()

    def notifyListeners(self) -> None:
        for l in self._listeners:
            l.documentChange()

    def getSelectedObjects(self) -> tuple:
        return self._roSelectedObjects

    def increaseZ(self, go: GraphicalObject) -> None:
        index = self._objects.index(go)
        if index < len(self._objects) - 1:
            self._objects[index], self._objects[index + 1] = self._objects[index + 1], self._objects[index]
        self._doBookkeeping()
        self.notifyListeners()

    def decreaseZ(self, go: GraphicalObject) -> None:
        index = self._objects.index(go)
        if index > 0:
            self._objects[index], self._objects[index - 1] = self._objects[index - 1], self._objects[index]
        self._doBookkeeping()
        self.notifyListeners()
    
    def findSelectedGraphicalObject(self, mousePoint: Point) -> int:
        for o in self._objects[::-1]:
            if o.selectionDistance(mousePoint) <= self._SELECTION_PROXIMITY:
                return o
        return None

    def findSelectedHotpoint(self, graphical_object: GraphicalObject, mousePoint: Point) -> int:
        for index in range(graphical_object.getNumberOfHotpoints()):
            distance = graphical_object.getHotPointDistance(index, mousePoint)
            if distance <= self._SELECTION_PROXIMITY:
                return index
        return -1


class Context(ABC):

    _state = None

    def __init__(self, state) -> None:
        self.transition_to(state)

    def transition_to(self, state):
        if self._state is not None:
            self._state.onLeaving()
        self._state = state
        self._state.context = self
        self._state.onEnter()

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        self._state.mouseDown(mousePoint, shiftDown, ctrlDown)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        self._state.mouseUp(mousePoint, shiftDown, ctrlDown)

    def mouseDragged(self, mousePoint: Point):
        self._state.mouseDragged(mousePoint)

    def keyPressed(self, keyChar: str):
        self._state.keyPressed(keyChar)

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        self._state.afterDraw(r, go)

    def onLeaving(self):
        self._state.onLeaving()


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def onEnter(self):
        pass

    @abstractmethod
    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    @abstractmethod
    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass
    @abstractmethod
    def mouseDragged(self, mousePoint: Point):
        pass

    @abstractmethod
    def keyPressed(self, keyChar: str):
        pass

    @abstractmethod
    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        pass

    @abstractmethod
    def onLeaving(self):
        pass


class IdleState(State):

    def onEnter(self):
        pass

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseDragged(self, mousePoint: Point):
        pass

    def keyPressed(self, keyChar: str):
        pass

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        pass

    def onLeaving(self):
        pass


class AddShapeState(State):
    
    _prototype: GraphicalObject
    _model: DocumentModel
    
    def __init__(self, prototype, model):
        self._prototype = prototype
        self._model = model

    def onEnter(self):
        pass

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        _new_graphical_object = self._prototype.duplicate()
        _new_graphical_object.translate(mousePoint)
        self._model.addGraphicalObject(_new_graphical_object)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseDragged(self, mousePoint: Point):
        pass

    def keyPressed(self, keyChar: str):
        pass

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        pass

    def onLeaving(self):
        pass


class SelectShapeState(State):
    
    _model: DocumentModel
    
    def __init__(self, model):
        self._model = model

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        if ctrlDown:
            selected_object = self._model.findSelectedGraphicalObject(mousePoint)
            if selected_object is not None:
                selected_object.setSelected(True)
        else:
            if len(self._model.getSelectedObjects()) == 1:
                selected_object = self._model.getSelectedObjects()[0]
                for hotpoint in range(selected_object.getNumberOfHotpoints()):
                    if selected_object.isHotPointSelected(hotpoint):
                        selected_object.setHotPointSelected(hotpoint, False)
                selected_hotpoint = self._model.findSelectedHotpoint(selected_object, mousePoint)
                if selected_hotpoint != -1:
                    selected_object.setHotPointSelected(selected_hotpoint, True)
                    return
            
            selected_object = self._model.findSelectedGraphicalObject(mousePoint)
            if selected_object is not None:
                for graphical_object in self._model.getSelectedObjects():
                    graphical_object.setSelected(False)
                selected_object.setSelected(True)
            if selected_object is None:
                for graphical_object in self._model.getSelectedObjects():
                    graphical_object.setSelected(False)
    
    def onEnter(self):
        pass

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseDragged(self, mousePoint: Point):
        if len(self._model.getSelectedObjects()) == 1:
                selected_object = self._model.getSelectedObjects()[0]
                for hotpoint in range(selected_object.getNumberOfHotpoints()):
                    if selected_object.isHotPointSelected(hotpoint):
                        selected_object.setHotPoint(hotpoint, mousePoint)
                        return


    def _move_composite(self, composite_object, hot_point_translate):
        for child in composite_object.getChildren():
            if isinstance(child, Composite):
                    self._move_composite(child, hot_point_translate)
            for hotpoint in range(child.getNumberOfHotpoints()):
                new_hotpoint = child.getHotPoint(hotpoint).translate(hot_point_translate)
                child.setHotPoint(hotpoint, new_hotpoint)
        self._model.notifyListeners()


    def keyPressed(self, keyChar: str):
        if keyChar in ['Up', 'Down', 'Left', 'Right']:
            if keyChar == 'Up':
                hot_point_translate = Point(0, -1)
            elif keyChar == 'Down':
                hot_point_translate = Point(0, 1)
            elif keyChar == 'Left':
                hot_point_translate = Point(-1, 0)
            elif keyChar == 'Right':
                hot_point_translate = Point(1, 0)
            for selected_object in self._model.getSelectedObjects():
                if isinstance(selected_object, Composite):
                    self._move_composite(selected_object, hot_point_translate)
                else:
                    for hotpoint in range(selected_object.getNumberOfHotpoints()):
                        new_hotpoint = selected_object.getHotPoint(hotpoint).translate(hot_point_translate)
                        selected_object.setHotPoint(hotpoint, new_hotpoint)
        elif keyChar == 'KP_Add':
            for selected_object in self._model.getSelectedObjects():
                self._model.increaseZ(selected_object)
        elif keyChar == 'KP_Subtract':
            for selected_object in self._model.getSelectedObjects():
                self._model.decreaseZ(selected_object)
        elif keyChar == 'g':
            self._context.transition_to(CompositeState(self._model, Composite(self._model.getSelectedObjects())))
        

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        if go is not None and go in self._model.getSelectedObjects():
            rectangle = go.getBoundingBox()
            points = []
            points.append(Point(rectangle.getX(), rectangle.getY()))
            points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY()))
            points.append(Point(rectangle.getX(), rectangle.getY() + rectangle.getHeight()))
            points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()))
            line_segments = [(points[0], points[1]),(points[0], points[2]),
                            (points[1], points[3]), (points[2], points[3])]
            for ls in line_segments:
                r.drawLine(ls[0], ls[1])
            if len(self._model.getSelectedObjects()) == 1:
                for i in range(go.getNumberOfHotpoints()):
                    hotpoint = go.getHotPoint(i)
                    points = []
                    points.append(Point(hotpoint.getX() - 3, hotpoint.getY() - 3))
                    points.append(Point(hotpoint.getX() + 3, hotpoint.getY() - 3))
                    points.append(Point(hotpoint.getX() - 3, hotpoint.getY() + 3))
                    points.append(Point(hotpoint.getX() + 3, hotpoint.getY() + 3))
                    line_segments = [(points[0], points[1]),(points[0], points[2]),
                                    (points[1], points[3]), (points[2], points[3])]
                    for ls in line_segments:
                        r.drawLine(ls[0], ls[1])

    def onLeaving(self):
        for graphical_object in self._model.getSelectedObjects():
            graphical_object.setSelected(False)


class Composite(AbstractGraphicalObject):
    
    def __init__(self, children=[]):
        super().__init__()
        self._children = children

    def getChildren(self):
        return self._children

    def add(self, component):
        self._children.append(component)
    
    def remove(self, component):
        self._children.remove(component)

    def selectionDistance(self, mousePoint: Point) -> float:
        rectangle = self.getBoundingBox()

        #Check if mousePoint is inside object
        rectangle_x_range = sorted([rectangle.getX(), rectangle.getX() + rectangle.getWidth()])
        rectangle_y_range = sorted([rectangle.getY(), rectangle.getY() + rectangle.getHeight()])
        if mousePoint.getX() >= rectangle_x_range[0] and mousePoint.getX() <= rectangle_x_range[1] and\
           mousePoint.getY() >= rectangle_y_range[0] and mousePoint.getY() <= rectangle_y_range[1]:
            return 0
        
        points = []
        points.append(Point(rectangle.getX(), rectangle.getY()))
        points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY()))
        points.append(Point(rectangle.getX(), rectangle.getY() + rectangle.getHeight()))
        points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()))
        line_segments = [(points[0], points[1]),(points[0], points[2]),
                         (points[1], points[3]), (points[2], points[3])]
        return min([GeometryUtil.distanceFromLineSegment(ls[0], ls[1], mousePoint) for ls in line_segments])

    def getBoundingBox(self) -> Rectangle:
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for child in self._children:
            rectangle = child.getBoundingBox()
            points = []
            points.append([rectangle.getX(), rectangle.getY()])
            points.append([rectangle.getX() + rectangle.getWidth(), rectangle.getY()])
            points.append([rectangle.getX(), rectangle.getY() + rectangle.getHeight()])
            points.append([rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()])
            sorted_x = sorted(points, key= lambda x: x[0])
            if min_x is None or sorted_x[0][0] < min_x:
                min_x = sorted_x[0][0]
            if max_x is None or sorted_x[-1][0] > max_x:
                max_x = sorted_x[-1][0]
            sorted_y = sorted(points, key= lambda x: x[1])
            if min_y is None or sorted_y[0][1] < min_y:
                min_y = sorted_y[0][1]
            if max_y is None or sorted_y[-1][1] > max_y:
                max_y = sorted_y[-1][1]
        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    def duplicate(self):
        return Composite(self._children)
    
    def getShapeName(self) -> str:
        return "Kompozit"

    def render(self, renderer) -> None:
        for child in self._children:
            child.render(renderer)

    def getShapeID(self) -> str:
        return '@COMP'

    def save(self, rows):
        for child in self.getChildren():
            child.save(rows)
        rows.append('{} {}'.format(self.getShapeID(), len(self.getChildren())))

    @staticmethod
    def load(stack, data):
        children = []
        for _ in range(int(data[0])):
            children.append(stack.pop())
        stack.push(Composite(children))


class CompositeState(State):

    _model: DocumentModel
    _composite: Composite

    def __init__(self, model, composite):
        self._model = model
        self._composite = composite

    def onEnter(self):
        for selected_object in self._model.getSelectedObjects():
            self._composite.add(selected_object)
            selected_object.setSelected(False)
            self._model.removeGraphicalObject(selected_object)
        self._model.addGraphicalObject(self._composite)
        self._composite.setSelected(True)
        
    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        pass

    def mouseDragged(self, mousePoint: Point):
        pass

    def _move_composite(self, composite_object, hot_point_translate):
        for child in composite_object.getChildren():
            if isinstance(child, Composite):
                    self._move_composite(child, hot_point_translate)
            for hotpoint in range(child.getNumberOfHotpoints()):
                new_hotpoint = child.getHotPoint(hotpoint).translate(hot_point_translate)
                child.setHotPoint(hotpoint, new_hotpoint)
        self._model.notifyListeners()

    def keyPressed(self, keyChar: str):
        if keyChar in ['Up', 'Down', 'Left', 'Right']:
            if keyChar == 'Up':
                hot_point_translate = Point(0, -1)
            elif keyChar == 'Down':
                hot_point_translate = Point(0, 1)
            elif keyChar == 'Left':
                hot_point_translate = Point(-1, 0)
            elif keyChar == 'Right':
                hot_point_translate = Point(1, 0)
            for selected_object in self._model.getSelectedObjects():
                if isinstance(selected_object, Composite):
                    self._move_composite(selected_object, hot_point_translate)
                else:
                    for hotpoint in range(selected_object.getNumberOfHotpoints()):
                        new_hotpoint = selected_object.getHotPoint(hotpoint).translate(hot_point_translate)
                        selected_object.setHotPoint(hotpoint, new_hotpoint)
        elif keyChar == 'KP_Add':
            for selected_object in self._model.getSelectedObjects():
                self._model.increaseZ(selected_object)
        elif keyChar == 'KP_Subtract':
            for selected_object in self._model.getSelectedObjects():
                self._model.decreaseZ(selected_object)
        elif keyChar == 'g':
            self._context.transition_to(CompositeState(self._model, Composite(self._model.getSelectedObjects())))
        elif keyChar == 'u':
            if len(self._model.getSelectedObjects()) == 1 and isinstance(self._model.getSelectedObjects()[0], Composite):
                for child in self._composite.getChildren():
                    self._model.addGraphicalObject(child)
                    child.setSelected(True)
                self._model.removeGraphicalObject(self._composite)
                self._context.transition_to(SelectShapeState(self._model))

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        if go is not None and go in self._model.getSelectedObjects():
            rectangle = go.getBoundingBox()
            points = []
            points.append(Point(rectangle.getX(), rectangle.getY()))
            points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY()))
            points.append(Point(rectangle.getX(), rectangle.getY() + rectangle.getHeight()))
            points.append(Point(rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()))
            line_segments = [(points[0], points[1]),(points[0], points[2]),
                            (points[1], points[3]), (points[2], points[3])]
            for ls in line_segments:
                r.drawLine(ls[0], ls[1])

    def onLeaving(self):
        pass


class EraserState(State):

    _model: DocumentModel

    def __init__(self, model, renderer):
        self._model = model
        self._renderer = renderer

    def onEnter(self):
        pass

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        self._last_point = mousePoint
        self._lines = []
        self._delete = set()

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool):
        for o in self._delete:
            self._model.removeGraphicalObject(o)

    def mouseDragged(self, mousePoint: Point):
        new_line = LineSegment(self._last_point, mousePoint)
        self._last_point = mousePoint
        selected_object = self._model.findSelectedGraphicalObject(mousePoint)
        new_line.render(self._renderer)
        if selected_object:
            self._delete.add(selected_object)
        self._lines.append(new_line)

    def keyPressed(self, keyChar: str):
        pass

    def afterDraw(self, r: Renderer, go: GraphicalObject = None):
        pass

    def onLeaving(self):
        pass


class CanvasRendererImpl(Renderer):
    _context: Context
    _canvas: tk.Canvas

    def __init__(self, canvas, context):
        self._canvas = canvas
        self._context = context

    def drawLine(self, s: Point, e: Point) -> None:
        self._canvas.create_line([s.getX(), s.getY(), e.getX(), e.getY()], fill='blue')

    def fillPolygon(self, points) -> None:
        draw_points = []
        for point in points:
            draw_points.extend([point.getX(), point.getY()])
        self._canvas.create_polygon(draw_points, outline='red', fill='blue')


class SVGRendererImpl(Renderer):


    def __init__(self, fileName):
        self._fileName = fileName
        self._lines = ['<svg xmlns="http://www.w3.org/2000/svg"\nxmlns:xlink="http://www.w3.org/1999/xlink">']

    def close(self):
        self._lines.append('</svg>')
        with open(self._fileName, 'w') as out:
            out.write('\n'.join(self._lines))
        self._lines = []

    def drawLine(self, s: Point, e: Point) -> None:
        self._lines.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="blue"/>\n'.format(s.getX(), s.getY(), e.getX(), e.getY()))

    def fillPolygon(self, points: list) -> None:
        line = '<polygon points="'
        line += ' '.join([str(point.getX()) + ',' + str(point.getY()) for point in points])
        line += '" style="stroke:red; fill:blue;"/>'
        self._lines.append(line)


class GUI(DocumentModelListener):

    _objects: list
    _window: tk.Tk
    _renderer: CanvasRendererImpl
    _document_model: DocumentModel
    _context: Context

    def __init__(self, objects):
        self._objects = objects
        self._window = tk.Tk()
        self._document_model = DocumentModel()
        self._document_model.addDocumentModelListener(self)
        self._context = Context(IdleState())
        self._initUI()

    def _initUI(self):
        self._window.geometry('860x600')
        self._window.title("Program za uređivanje vektorskih crteža")
        self._window.bind('<Escape>', lambda event: self._context.transition_to(IdleState()))
        self._window.bind('<Key>', lambda event: self._context.keyPressed(event.keysym))
        self._window.bind('<g>', lambda event: self._context.keyPressed(event.keysym))
        self._window.bind('<u>', lambda event: self._context.keyPressed(event.keysym))
        #Init toolbar
        toolbar = tk.Frame(self._window, bd=1, relief=tk.RAISED)
        tk.Button(toolbar, text="Učitaj", command= lambda: self._load()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Pohrani", command= lambda: self._save()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="SVG export", command= lambda: self._svg_export()).pack(side=tk.LEFT)
        for o in self._objects:
            tk.Button(toolbar, text=o.getShapeName(), command= lambda ob=o:
                      self._context.transition_to(AddShapeState(ob, self._document_model))).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Selektiraj", command= lambda: self._context.transition_to(SelectShapeState(self._document_model))).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Brisalo", command= lambda: self._context.transition_to(EraserState(self._document_model, self._renderer))).pack(side=tk.LEFT)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        #Init canvas
        frame = tk.Frame(self._window)
        frame.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(frame)
        self.canvas.bind("<Button-1>", lambda event: self._context.mouseDown(Point(event.x, event.y), False, False))
        self.canvas.bind("<Control-Button-1>", lambda event: self._context.mouseDown(Point(event.x, event.y), False, True))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self._context.mouseUp(Point(event.x, event.y), False, False))
        self.canvas.bind("<Control-ButtonRelease-1>", lambda event: self._context.mouseUp(Point(event.x, event.y), False, True))
        self.canvas.bind("<B1-Motion>", lambda event: self._context.mouseDragged(Point(event.x, event.y)))

        self.canvas.pack(fill=tk.BOTH, expand=1)

        self._renderer = CanvasRendererImpl(self.canvas, self._context)
        self._window.mainloop()


    def _svg_export(self):
        f = tkinter.filedialog.asksaveasfilename(filetypes=[('Scalable Vector Graphics','*.svg')])
        if f is not None:
            renderer = SVGRendererImpl(f)
            for o in self._document_model.list():
                o.render(renderer)
            renderer.close()
    
    def _save(self):
        f = tkinter.filedialog.asksaveasfilename(filetypes=[('Text file','*.txt')])
        if f is not None:
            rows = []
            for o in self._document_model.list():
                o.save(rows)
            with open(f, 'w') as out:
                out.write('\n'.join(rows))

    
    def _load(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.Open(filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            lineStack = Stack()
            with open(fl, 'r') as inp:
                for line in inp:
                    line = line.strip().split(' ')
                    if line[0] == '@LINE':
                        LineSegment.load(lineStack, line[1:])
                    if line[0] == '@OVAL':
                        Oval.load(lineStack, line[1:])
                    if line[0] == '@COMP':
                        Composite.load(lineStack, line[1:])
        
        while not lineStack.empty():
            go = lineStack.pop()
            self._document_model.addGraphicalObject(go)
        
    def documentChange(self) -> None:
        self.canvas.delete("all")
        for graphical_object in self._document_model.list():
            graphical_object.render(self._renderer)
            self._context.afterDraw(self._renderer, graphical_object)
        self._context.afterDraw(self._renderer)


def main():
    objects = []
    objects.append(LineSegment())
    objects.append(Oval())

    GUI(objects)

if __name__ == "__main__":
    main()    