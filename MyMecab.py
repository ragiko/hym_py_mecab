# coding: utf-8

import MeCab
from NodeWrapper import NodeWrapper
# import時にはfromを書く
# 参考: http://www.python-izm.com/contents/basis/import.shtml

class MecabParser:
    """
    文書を形態素解析し、単語を抽出するモジュール
    """

    def __init__(self, doc):
        """
        _tagger: mecabのtagger
        _doc: 解析する文書 (unicode)
        _node_wrappers_cache: 形態素解析結果を一時的に保存
        """

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
        """
        nodeの解析結果を一時保存するcacheに入れる
        """
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
    
    def find_words_by_pos(self, pos_set, is_base_word = False):
        """
        pos(品詞)から品詞にあった単語を取得

        pos_set: 品詞の集合
        """
        if (len(self._node_wrappers_cache) == 0):
            # メソッドは、 self 引数のメソッド属性を使って、他のメソッドを呼び出すことができます
            # 参考: http://docs.python.jp/2/tutorial/classes.html
            self.save_node_wrappers()

        node_wrappers = self._node_wrappers_cache


        if (len(pos_set) == 0):
            # pos_setが0の時は全ての単語を返却
            base_and_surface_pair = [(nw.base, nw.surface) for nw in node_wrappers]
            return [self.choose_base_or_surface_word(pair, is_base_word) for pair in base_and_surface_pair]
        else:
            base_and_surface_pair = [(nw.base, nw.surface) for nw in node_wrappers if nw.pos in pos_set]
            return [self.choose_base_or_surface_word(pair, is_base_word) for pair in base_and_surface_pair]

    def choose_base_or_surface_word(self, base_and_surface_pair, is_base_word):
        """
        品詞の原型か活用形かを選ぶ関数
        """
        base = base_and_surface_pair[0] 
        surface = base_and_surface_pair[1] 

        if (is_base_word):
            # mecabは原型の時に*を返却する時があるため、その場合は活用形を使う 
            return surface if base == u'*' else base # return base
        else:
            return surface # return surface

if __name__ == "__main__":
    doc = u'MeCabで遊んでみよう！'
    mp = MecabParser(doc)

    mp.parse_dump()
    # MeCab, 名詞, 一般, *, *, *, *, *
    # で, 助詞, 格助詞, 一般, *, *, *, で
    # 遊ん, 動詞, 自立, *, *, 五段・バ行, 連用タ接続, 遊ぶ
    # で, 助詞, 接続助詞, *, *, *, *, で
    # みよ, 動詞, 非自立, *, *, 一段, 未然ウ接続, みる
    # う, 助動詞, *, *, *, 不変化型, 基本形, う
    # ！, 記号, 一般, *, *, *, *, ！

    # -------------------- 
    # 名詞を抽出
    # -------------------- 
    pos_set = set([u"名詞"])
    node_wrappers = mp.find_words_by_pos(pos_set, False)
    for n in node_wrappers:
        print n.encode("utf-8")
    # MeCab

    # -------------------- 
    # 名詞・動詞を抽出
    # -------------------- 
    pos_set = set([u"名詞", u"動詞"])
    node_wrappers = mp.find_words_by_pos(pos_set, False)
    for n in node_wrappers:
        print n.encode("utf-8")
    # MeCab
    # 遊ん
    # みよ

    # -------------------- 
    # 品詞全てを抽出
    # -------------------- 
    pos_set = set([])
    node_wrappers = mp.find_words_by_pos(pos_set, False)
    for n in node_wrappers:
        print n.encode("utf-8")
    # MeCab
    # で
    # 遊ん
    # で
    # みよ
    # う
    # ！

    # -------------------- 
    # 名詞・動詞(原型)を抽出
    # -------------------- 
    pos_set = set([u"名詞", u"動詞"])
    node_wrappers = mp.find_words_by_pos(pos_set, True)
    for n in node_wrappers:
        print n.encode("utf-8")
    # MeCab
    # 遊ぶ
    # みる

