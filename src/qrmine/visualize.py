"""
Copyright (C) 2025 Bell Eapen

This file is part of qrmine.

qrmine is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

qrmine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with qrmine.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import Counter

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
from sklearn.manifold import TSNE
from wordcloud import STOPWORDS, WordCloud


class QRVisualize:
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize the QRVisualize class with a DataFrame.

        Parameters:
        data (pd.DataFrame): The DataFrame containing the data to visualize.
        """
        self.data = data

    def plot_frequency_distribution_of_words(self, df=None, folder_path=None):
        if df is None:
            df = self.data
        doc_lens = [len(d) for d in df.Text]

        # Plot
        plt.figure(figsize=(16, 7), dpi=160)
        plt.hist(doc_lens, bins=1000, color="navy")
        plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
        plt.text(750, 90, "Median : " + str(round(np.median(doc_lens))))
        plt.text(750, 80, "Stdev   : " + str(round(np.std(doc_lens))))
        plt.text(750, 70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
        plt.text(750, 60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

        plt.gca().set(
            xlim=(0, 1000), ylabel="Number of Documents", xlabel="Document Word Count"
        )
        plt.tick_params(size=16)
        plt.xticks(np.linspace(0, 1000, 9))
        plt.title("Distribution of Document Word Counts", fontdict=dict(size=22))
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def plot_distribution_by_topic(self, df=None, folder_path=None):
        if df is None:
            df = self.data
        # Plot
        cols = [
            color for name, color in mcolors.TABLEAU_COLORS.items()
        ]  # more colors: 'mcolors.XKCD_COLORS'

        fig, axes = plt.subplots(
            2, 2, figsize=(16, 14), dpi=160, sharex=True, sharey=True
        )

        for i, ax in enumerate(axes.flatten()):
            df_dominant_topic_sub = df.loc[df.Dominant_Topic == i, :]
            doc_lens = [len(d) for d in df_dominant_topic_sub.Text]
            ax.hist(doc_lens, bins=1000, color=cols[i])
            ax.tick_params(axis="y", labelcolor=cols[i], color=cols[i])
            sns.kdeplot(
                doc_lens, color="black", fill=False, ax=ax.twinx(), warn_singular=False
            )
            ax.set(xlim=(0, 1000), xlabel="Document Word Count")
            ax.set_ylabel("Number of Documents", color=cols[i])
            ax.set_title("Topic: " + str(i), fontdict=dict(size=16, color=cols[i]))

        fig.tight_layout()
        fig.subplots_adjust(top=0.90)
        plt.xticks(np.linspace(0, 1000, 9))
        fig.suptitle(
            "Distribution of Document Word Counts by Dominant Topic", fontsize=22
        )
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def plot_wordcloud(self, topics=None, folder_path=None):
        cols = [
            color for name, color in mcolors.TABLEAU_COLORS.items()
        ]  # more colors: 'mcolors.XKCD_COLORS'

        cloud = WordCloud(
            stopwords=STOPWORDS,
            background_color="white",
            width=250,
            height=180,
            max_words=5,
            colormap="tab10",
            color_func=lambda *args, **kwargs: cols[i],
            prefer_horizontal=1.0,
        )

        fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            fig.add_subplot(ax)
            topic_words = dict(topics[i][1])
            cloud.generate_from_frequencies(topic_words, max_font_size=300)
            plt.gca().imshow(cloud)
            plt.gca().set_title("Topic " + str(i), fontdict=dict(size=16))
            plt.gca().axis("off")

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.axis("off")
        plt.margins(x=0, y=0)
        plt.tight_layout()
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def plot_importance(self, topics=None, processed_docs=None, folder_path=None):
        data_flat = [w for w_list in processed_docs for w in w_list]
        counter = Counter(data_flat)

        out = []
        for i, topic in topics:
            for word, weight in topic:
                out.append([word, i, weight, counter[word]])

        df = pd.DataFrame(out, columns=["word", "topic_id", "importance", "word_count"])

        # Plot Word Count and Weights of Topic Keywords
        fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharey=True, dpi=160)
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
        for i, ax in enumerate(axes.flatten()):
            ax.bar(
                x="word",
                height="word_count",
                data=df.loc[df.topic_id == i, :],
                color=cols[i],
                width=0.5,
                alpha=0.3,
                label="Word Count",
            )
            ax_twin = ax.twinx()
            ax_twin.bar(
                x="word",
                height="importance",
                data=df.loc[df.topic_id == i, :],
                color=cols[i],
                width=0.2,
                label="Weights",
            )
            ax.set_ylabel("Word Count", color=cols[i])
            ax_twin.set_ylim(0, 0.030)
            ax.set_ylim(0, 3500)
            ax.set_title("Topic: " + str(i), color=cols[i], fontsize=16)
            ax.tick_params(axis="y", left=False)
            ax.set_xticklabels(
                df.loc[df.topic_id == i, "word"],
                rotation=30,
                horizontalalignment="right",
            )
            ax.legend(loc="upper left")
            ax_twin.legend(loc="upper right")

        fig.tight_layout(w_pad=2)
        fig.suptitle("Word Count and Importance of Topic Keywords", fontsize=22, y=1.05)
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def sentence_chart(self, lda_model=None, corpus=None, start=0, end=13, folder_path=None):
        if lda_model is None:
            raise ValueError("LDA model is not provided.")
        corp = corpus[start:end]
        mycolors = [color for name, color in mcolors.TABLEAU_COLORS.items()]

        fig, axes = plt.subplots(
            end - start, 1, figsize=(20, (end - start) * 0.95), dpi=160
        )
        axes[0].axis("off")
        for i, ax in enumerate(axes):
            try:
                if i > 0:
                    corp_cur = corp[i - 1]
                    topic_percs, wordid_topics, _ = lda_model[corp_cur]
                    word_dominanttopic = [
                        (lda_model.id2word[wd], topic[0]) for wd, topic in wordid_topics
                    ]
                    ax.text(
                        0.01,
                        0.5,
                        "Doc " + str(i - 1) + ": ",
                        verticalalignment="center",
                        fontsize=16,
                        color="black",
                        transform=ax.transAxes,
                        fontweight=700,
                    )

                    # Draw Rectange
                    topic_percs_sorted = sorted(
                        topic_percs, key=lambda x: (x[1]), reverse=True
                    )
                    ax.add_patch(
                        Rectangle(
                            (0.0, 0.05),
                            0.99,
                            0.90,
                            fill=None,
                            alpha=1,
                            color=mycolors[topic_percs_sorted[0][0]],
                            linewidth=2,
                        )
                    )

                    word_pos = 0.06
                    for j, (word, topics) in enumerate(word_dominanttopic):
                        if j < 14:
                            ax.text(
                                word_pos,
                                0.5,
                                word,
                                horizontalalignment="left",
                                verticalalignment="center",
                                fontsize=16,
                                color=mycolors[topics],
                                transform=ax.transAxes,
                                fontweight=700,
                            )
                            word_pos += 0.009 * len(
                                word
                            )  # to move the word for the next iter
                            ax.axis("off")
                    ax.text(
                        word_pos,
                        0.5,
                        ". . .",
                        horizontalalignment="left",
                        verticalalignment="center",
                        fontsize=16,
                        color="black",
                        transform=ax.transAxes,
                    )
            except:
                continue

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.suptitle(
            "Sentence Topic Coloring for Documents: "
            + str(start)
            + " to "
            + str(end - 2),
            fontsize=22,
            y=0.95,
            fontweight=700,
        )
        plt.tight_layout()
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def cluster_chart(self, lda_model=None, corpus=None, n_topics=3, folder_path=None):
        # Get topic weights
        topic_weights = []
        for i, row_list in enumerate(lda_model[corpus]):
            topic_weights.append([w for i, w in row_list[0]])

        # Array of topic weights
        arr = pd.DataFrame(topic_weights).fillna(0).values

        # Keep the well separated points (optional)
        arr = arr[np.amax(arr, axis=1) > 0.35]

        # Dominant topic number in each doc
        topic_num = np.argmax(arr, axis=1)

        # tSNE Dimension Reduction
        tsne_model = TSNE(
            n_components=2, verbose=1, random_state=0, angle=0.99, init="pca"
        )
        tsne_lda = tsne_model.fit_transform(arr)

        # Plot
        plt.figure(figsize=(16, 10), dpi=160)
        for i in range(n_topics):
            plt.scatter(
                tsne_lda[topic_num == i, 0],
                tsne_lda[topic_num == i, 1],
                label=str(i),
                alpha=0.5,
            )
        plt.title("t-SNE Clustering of Topics", fontsize=22)
        plt.xlabel("t-SNE Dimension 1", fontsize=16)
        plt.ylabel("t-SNE Dimension 2", fontsize=16)
        plt.legend(title="Topic Number", loc="upper right")
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def most_discussed_topics(
        self, lda_model, dominant_topics, topic_percentages, folder_path=None
    ):

        # Distribution of Dominant Topics in Each Document
        df = pd.DataFrame(dominant_topics, columns=["Document_Id", "Dominant_Topic"])
        dominant_topic_in_each_doc = df.groupby("Dominant_Topic").size()
        df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(
            name="count"
        ).reset_index()

        # Total Topic Distribution by actual weight
        topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
        df_topic_weightage_by_doc = (
            topic_weightage_by_doc.sum().to_frame(name="count").reset_index()
        )

        # Top 3 Keywords for each Topic
        topic_top3words = [
            (i, topic)
            for i, topics in lda_model.show_topics(formatted=False)
            for j, (topic, wt) in enumerate(topics)
            if j < 3
        ]

        df_top3words_stacked = pd.DataFrame(
            topic_top3words, columns=["topic_id", "words"]
        )
        df_top3words = df_top3words_stacked.groupby("topic_id").agg(", \n".join)
        df_top3words.reset_index(level=0, inplace=True)

        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=120, sharey=True)

        # Topic Distribution by Dominant Topics
        ax1.bar(
            x="Dominant_Topic",
            height="count",
            data=df_dominant_topic_in_each_doc,
            width=0.5,
            color="firebrick",
        )
        ax1.set_xticks(
            range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__())
        )
        tick_formatter = FuncFormatter(
            lambda x, pos: "Topic "
            + str(x)
            + "\n"
            + df_top3words.loc[df_top3words.topic_id == x, "words"].values[0]
        )
        ax1.xaxis.set_major_formatter(tick_formatter)
        ax1.set_title("Number of Documents by Dominant Topic", fontdict=dict(size=10))
        ax1.set_ylabel("Number of Documents")
        ax1.set_ylim(0, 1000)

        # Topic Distribution by Topic Weights
        ax2.bar(
            x="index",
            height="count",
            data=df_topic_weightage_by_doc,
            width=0.5,
            color="steelblue",
        )
        ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
        ax2.xaxis.set_major_formatter(tick_formatter)
        ax2.set_title("Number of Documents by Topic Weightage", fontdict=dict(size=10))

        plt.show()

        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()
