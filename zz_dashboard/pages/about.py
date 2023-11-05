from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    name='About',
    top_nav=True,
    path='/'
)


def layout():
    layout = dbc.Container([
        html.H1('About this App', className='mt-3'),
        html.Hr(className="my-2"),
        html.H5('How to ...'),
        html.P(["Download model weights from ",
                html.A("ml-jku/mae-ct",
                       href="https://github.com/ml-jku/mae-ct"),
                " and ",
                html.A("vit_analysis",
                       href="http://www.cs.umd.edu/~sakshams/vit_analysis/"),
                       " and follow the installation instructions."]),
        html.P(
            ["Store it in the 'repo_root/models/[model_name]', e.g:  '/vit_analysis/models/mae'"]),
        html.P(["To perform the attention analysis, download the ImageNet-50 subset. The list of data names is stored in '/vit_analysis/data/imagenet_50.txt'"]),
        
        
        html.P(["For more information, see the links below."]),
        html.H5('About The Data Source'),
        html.P(["Homepage of ",
                html.A("ImageNet",
                       href="https://www.image-net.org/"),
                ]),
        html.P(["Download the ImageNet data from ",
                html.A("Kaggle",
                       href="https://www.kaggle.com/c/imagenet-object-localization-challenge/overview/description"),
                ]),

        html.H5('Read More'),
        html.P(["Click for more information: ",
                html.A("vit_analysis",
                       href="http://www.cs.umd.edu/~sakshams/vit_analysis/"),
                ]),
        html.P(["Click for more information: ",
                html.A("ml-jku/mae-ct",
                       href="https://github.com/ml-jku/mae-ct"),
                ]),
    ])
    return layout
