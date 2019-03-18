import subprocess


class Qrmine(object):

    def __init__(self):
        self._content = ""
        self._min_occurrence_for_topic = 2
        self._common_verbs = 10

    def min_topic(self, min_topic):
        self._min_occurrence_for_topic = min_topic

    def common_verbs(self, common_verbs):
        self._common_verbs = common_verbs

    @staticmethod
    def print_table(table):
        col_width = [max(len(x) for x in col) for col in zip(*table)]
        for line in table:
            print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                    for i, x in enumerate(line)) + " |")

    @property
    def get_git_revision_hash(self):
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'])

    @property
    def get_git_revision_short_hash(self):
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8")
        # return subprocess.check_output(['git', 'log', '-1', '--format=%cd']).strip().decode("utf-8")[10:]

    def print_categories(self, doc):
        bot = doc.to_bag_of_terms(ngrams=(2, 3), named_entities=True, normalize='lemma', weighting='count',
                                  as_strings=True, filter_stops=True, filter_punct=True, filter_nums=True, min_freq=2)
        categories = sorted(bot.items(), key=lambda x: x[1], reverse=True)[:15]
        output = []
        print("\n---Categories with count---")
        output.append(("CATEGORY", "COUNT"))
        for category, count in categories:
            output.append((category, str(count)))
        self.print_table(output)
        print("---------------------------\n")

    def print_topics(self, model, vectorizer, number_topics):
        topic_list = list(range(1, number_topics))
        output = []
        print("\n---Topics---")
        output.append(("TOPIC", "DESCRIPTION"))
        for topic_idx, top_terms in model.top_topic_terms(vectorizer.id_to_term, topics=topic_list):
            output.append(("TOPIC:" + str(topic_idx), '   '.join(top_terms)))
        self.print_table(output)
        print("---------------------------\n")

    def print_documents(self, model, corpus, doc_topic_matrix, number_topics):
        topic_list = list(range(1, number_topics))
        output = []
        print("\n---Topics---")
        output.append(("TOPIC", "DOCUMENTS"))
        for topic_idx, top_docs in model.top_topic_docs(doc_topic_matrix, topics=topic_list,
                                                        top_n=self._min_occurrence_for_topic):
            str_topic_idx = str(topic_idx)
            for j in top_docs:
                output.append((str_topic_idx, corpus[j].metadata['title']))
                str_topic_idx = "..."
        self.print_table(output)
        print("---------------------------\n")

    def print_dict(self, content):
        output = []
        print("\n---Coding Dictionary---")
        output.append(("CATEGORY", "PROPERTY", "DIMENSION"))
        words = content.common_verbs(self._common_verbs)
        for word, f1 in words:
            for attribute, f2 in content.attributes(word, 3):
                for dimension, f3 in content.dimensions(attribute, 3):
                    output.append((word, attribute, dimension))
                    word = '...'
                    attribute = '...'

        self.print_table(output)
        print("---------------------------\n")
