import os

import folium


SAMPLE_DATA_LOCATION = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_space_separated_data.txt')

JAVASCRIPT_REFRESH_PAGE = """
<script type="text/javascript">
    function refresh() {
        window.location.reload(true);
        setTimeout(refresh, 30000);
        console.log('page refreshed!')
    }
    setTimeout(refresh, 30000);
</script>
"""

def extend_html_page(page_name, content):
    with open(os.path.join(os.path.dirname(__file__), '..', page_name), 'a+') as html:
        html.write(content)

def get_data():
    with open(SAMPLE_DATA_LOCATION) as f:
        header = f.readline().strip('\n').split(' ')

        for line in f.readlines():
            line = line.strip('\n').split(' ')
            yield dict(zip(header, line))


def generate_map():
    my_map = folium.Map(location=[47, 7], zoom_start=6)
    feature_group = folium.FeatureGroup("My Map")

    try:
        for data in get_data():
            feature_group.add_child(folium.Marker(location=[float(data['latitude']), float(data['longitude'])],
                                                  popup=data['imageName'],
                                                  icon=folium.Icon(color='green')))
        # draw the map here
        my_map.add_child(feature_group)
        my_map.save('index.html')

        # add extra script to refresh map
        # extend_html_page('index.html', JAVASCRIPT_REFRESH_PAGE)

    except StopIteration:
        print('Done processing the maps')
    except Exception as e:
        print('oops, something is OFF!', e)


if __name__ == '__main__':
    generate_map()
