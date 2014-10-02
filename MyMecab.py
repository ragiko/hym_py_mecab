# coding: utf-8

import MeCab


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
		self.surface = node.surface.decode("utf-8")
		node_array = node.feature.split(",")

		self.pos = node_array[0].decode("utf-8")
		self.pos_detail1 = node_array[1].decode("utf-8")
		self.pos_detail2 = node_array[2].decode("utf-8")
		self.pos_detail3 = node_array[3].decode("utf-8")
		self.conj_form = node_array[4].decode("utf-8")
		self.conj_type = node_array[5].decode("utf-8")
		self.base = node_array[6].decode("utf-8")

		if len(node_array) > 7:
			self.read = node_array[7].decode("utf-8")
			self.pron = node_array[8].decode("utf-8")

class MecabParser:
    def __init__(self, doc):
        self._tagger = MeCab.Tagger('')
        self._doc = doc # unicode
        self._node_wrappers_cache = []
    
    def parse_dump(self):
        """
        Mecabの解析結果をdumpする関数
        """
        if (len(self._node_wrappers_cache) == 0):
            self.save_node_wrappers()
        
        node_wrappers = self._node_wrappers_cache

        for nw in node_wrappers:
            print "%s, %s, %s, %s, %s, %s, %s, %s" % (
                    nw.surface.encode("utf-8"),
                    nw.pos.encode("utf-8"),
                    nw.pos_detail1.encode("utf-8"),
                    nw.pos_detail2.encode("utf-8"),
                    nw.pos_detail3.encode("utf-8"),
                    nw.conj_form.encode("utf-8"),
                    nw.conj_type.encode("utf-8"),
                    nw.base.encode("utf-8")
                    )
        
    def save_node_wrappers(self):
        # http://shogo82148.github.io/blog/2012/12/15/mecab-python/
        # MeCabに渡す文字列はencode，戻ってきた文字列はdecodeする
        # MeCabに渡した文字列は必ず変数に入れておく
        encoded_text = self._doc.encode('utf-8')
        node = self._tagger.parseToNode(encoded_text) # 変数に入れる！

        node_wrappers = []
        while node:
            # BOS/EOSを除く
            if (node.feature[0:7] == 'BOS/EOS'):
                node = node.next
                continue
            
            node_wrappers.append(NodeWrapper(node))
            node = node.next

        self._node_wrappers_cache = node_wrappers
    

    
    def find_words_by_pos(self, pos_set):

        if (len(self._node_wrappers_cache) == 0):
            # メソッドは、 self 引数のメソッド属性を使って、他のメソッドを呼び出すことができます
            # 参考: http://docs.python.jp/2/tutorial/classes.html
            self.save_node_wrappers()

        node_wrappers = self._node_wrappers_cache

        if (len(pos_set) == 0):
            # pos_setが0の時は全ての単語を返却
            return [nw.surface for nw in node_wrappers]
        else:
            return [nw.surface for nw in node_wrappers if nw.pos in pos_set]
        

if __name__ == "__main__":
    doc = u'MeCabで遊んでみよう！'
    mp = MecabParser(doc)
    mp.parse_dump()

    pos_set = set([u"名詞", u"動詞", u"助詞"])
    node_wrappers = mp.find_words_by_pos(pos_set)

    for n in node_wrappers:
        print n.encode("utf-8")


    

