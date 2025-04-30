import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.colors as mcolors

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
        plt.figure(figsize=(16,7), dpi=160)
        plt.hist(doc_lens, bins = 1000, color='navy')
        plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
        plt.text(750,  90, "Median : " + str(round(np.median(doc_lens))))
        plt.text(750,  80, "Stdev   : " + str(round(np.std(doc_lens))))
        plt.text(750,  70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
        plt.text(750,  60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

        plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
        plt.tick_params(size=16)
        plt.xticks(np.linspace(0,1000,9))
        plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()

    def plot_distribution_by_topic(self, df=None, folder_path=None):
        if df is None:
            df = self.data
        # Plot
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

        fig, axes = plt.subplots(2,2,figsize=(16,14), dpi=160, sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            df_dominant_topic_sub = df.loc[df.Dominant_Topic == i, :]
            doc_lens = [len(d) for d in df_dominant_topic_sub.Text]
            ax.hist(doc_lens, bins = 1000, color=cols[i])
            ax.tick_params(axis='y', labelcolor=cols[i], color=cols[i])
            sns.kdeplot(doc_lens, color="black", shade=False, ax=ax.twinx())
            ax.set(xlim=(0, 1000), xlabel='Document Word Count')
            ax.set_ylabel('Number of Documents', color=cols[i])
            ax.set_title('Topic: '+str(i), fontdict=dict(size=16, color=cols[i]))

        fig.tight_layout()
        fig.subplots_adjust(top=0.90)
        plt.xticks(np.linspace(0,1000,9))
        fig.suptitle('Distribution of Document Word Counts by Dominant Topic', fontsize=22)
        plt.show()
        # save
        if folder_path:
            plt.savefig(folder_path)
            plt.close()