# coding: utf-8

class NodeWrapper:
    """
    nodeのデータを構造化
    参考: http://yshtak.tumblr.com/post/26010459591/python-mecab

	surface:表層
    pos: 品詞
    pos_detail1: 品詞細分類1
    pos_detail2: 品詞細分類2
    pos_detail3: 品詞細分類3
    conj_form: 活用型
    conj_type: 活用形
    base: 基本形
    read: 読み (もし存在するなら)
    pron: 発音 (もし存在するなら)
    """

    def __init__(self, node):
		self.surface = node.surface
		node_array = node.feature.split(",")

		self.pos = []
		self.pos = node_array[0]
		self.pos_detail1 = node_array[1]
		self.pos_detail2 = node_array[2]
		self.pos_detail3 = node_array[3]
		self.conj_form = node_array[4]
		self.conj_type = node_array[5]
		self.base = node_array[6]

		if len(node_array) > 7:
			self.read = node_array[7]
			self.pron = node_array[8]

