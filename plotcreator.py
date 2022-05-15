import matplotlib.pyplot as plt

class Plotcreator:

  def linear_plot(self,x,y,filename):
    '''
    saves image of matplotlib's linear plot
    :param x: first collumns to plot
    :param y: second collumns to plot
    :param filename: fileid

    '''
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.figure(facecolor='#082032')
    ax = plt.axes()
    ax.set_facecolor("yellow")
    plt.plot(x, y, color="#FF4C29")
    ax.xaxis.label.set_color('red')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.savefig('static/{}.png'.format(filename))
    plt.close()

  def scatter(self,x,y,filename):
    '''
    saves image of matplotlib's scatter plot
    :param x: first collumns to plot
    :param y: second collumns to plot
    :param filename: fileid

    '''
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.figure(facecolor='#082032')
    ax = plt.axes()
    ax.set_facecolor("yellow")
    plt.scatter(x, y, color="#FF4C29")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.savefig('static/{}.png'.format(filename))
    plt.close()

  def barplot(self, x, y, filename):
    '''
    saves image of matplotlib's bar plot
    :param x: first collumns to plot
    :param y: second collumns to plot
    :param filename: fileid

    '''
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.figure(facecolor='#082032')
    ax = plt.axes()
    ax.set_facecolor("yellow")
    plt.bar(x, y, color="#FF4C29")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.savefig('static/{}.png'.format(filename))
    plt.close()