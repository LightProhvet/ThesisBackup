# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robot_ros2_msgs:msg/Encoders.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Encoders(type):
    """Metaclass of message 'Encoders'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robot_ros2_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robot_ros2_msgs.msg.Encoders')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__encoders
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__encoders
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__encoders
            cls._TYPE_SUPPORT = module.type_support_msg__msg__encoders
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__encoders

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Encoders(metaclass=Metaclass_Encoders):
    """Message class 'Encoders'."""

    __slots__ = [
        '_header',
        '_right_front',
        '_left_front',
        '_left_back',
        '_right_back',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'right_front': 'float',
        'left_front': 'float',
        'left_back': 'float',
        'right_back': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.right_front = kwargs.get('right_front', float())
        self.left_front = kwargs.get('left_front', float())
        self.left_back = kwargs.get('left_back', float())
        self.right_back = kwargs.get('right_back', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.right_front != other.right_front:
            return False
        if self.left_front != other.left_front:
            return False
        if self.left_back != other.left_back:
            return False
        if self.right_back != other.right_back:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def right_front(self):
        """Message field 'right_front'."""
        return self._right_front

    @right_front.setter
    def right_front(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'right_front' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'right_front' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._right_front = value

    @builtins.property
    def left_front(self):
        """Message field 'left_front'."""
        return self._left_front

    @left_front.setter
    def left_front(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'left_front' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'left_front' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._left_front = value

    @builtins.property
    def left_back(self):
        """Message field 'left_back'."""
        return self._left_back

    @left_back.setter
    def left_back(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'left_back' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'left_back' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._left_back = value

    @builtins.property
    def right_back(self):
        """Message field 'right_back'."""
        return self._right_back

    @right_back.setter
    def right_back(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'right_back' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'right_back' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._right_back = value
