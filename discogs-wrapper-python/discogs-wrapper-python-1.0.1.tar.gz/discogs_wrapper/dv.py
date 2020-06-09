from . import session

class DV(object):
    def __init__(self,unique_word):
        self.unique_word = unique_word

    def get_release(self,id,curr_abbr =''):
        path = 'https://api.discogs.com/releases/{}'.format(id)
        session.params['user-agent'] = self.unique_word
        if curr_abbr!='':
            session.params['curr_abbr'] = curr_abbr
        response = session.get(path)
        return response.json()

    #TODO: update the put release method

    def delete_release_user(self,release_id,username,token=''):
        path = 'https://api.discogs.com/releases/{}/rating/{}'.format(release_id,username)
        session.params['user-agent'] = self.unique_word
        session.params['token'] = token
        response = session.delete(path)
        return response

    def get_release_rating_by_user(self,release_id,username):
        path = 'https://api.discogs.com/releases/{}/rating/{}'.format(release_id,username)
        session.params['user-agent'] = self.unique_word
        response = session.get(path)
        return response.json()

    def get_community_release_rating(self,release_id):
        path = 'https://api.discogs.com/releases/{}/rating'.format(release_id)
        session.params['user-agent'] = self.unique_word
        response = session.get(path)
        return response.json()

    def get_masters_release(self,master_id):
        path = 'https://api.discogs.com/masters/{}'.format(master_id)
        response = session.get(path)
        session.params['user-agent'] = self.unique_word
        return response.json()

    def get_masters_release_version(self,master_id,page='',per_page=''):
        path = 'https://api.discogs.com/masters/{}/versions'.format(master_id)
        session.params['user-agent'] = self.unique_word
        if page!='':
            session.params['page'] = page
        if per_page!='':
            session.params['per_page'] = per_page
        response = session.get(path)
        return response.json()
        

    def get_artist(self,artist_id):
        path = 'https://api.discogs.com/artists/{}'.format(artist_id)
        response = session.get(path)
        session.params['user-agent'] = self.unique_word
        return response.json()

    def get_artist_releases(self,artist_id,sort='',sort_order=''):
        path = 'https://api.discogs.com/artists/{}/releases'.format(artist_id)
        if sort!='':
            session.params['sort'] = sort
        if sort_order!='':
            session.params['sort_order'] = sort_order
        session.params['user-agent'] = self.unique_word
        response = session.get(path)
        return response.json()


    def get_label(self,label_id):
        path = 'https://api.discogs.com/labels/{}'.format(label_id)
        response = session.get(path)
        session.params['user-agent'] = self.unique_word
        return response.json()

    #TODO: test from this point

    def get_all_label_releases(self,label_id,page='',per_page=''):
        path = 'https://api.discogs.com/labels/{}/releases{}'.format(label_id)
        session.params['user-agent'] = self.unique_word
        if page!='':
            session.params['page'] = page
        if per_page!='':
            session.params['per_page'] = per_page
        response = session.get(path)
        return response.json()

    def get_search(self,q='',token='',title='',typee='',release_title='',credit='',artist='',anv='',label='',genre='',style='',country='',year='',formatt = '',catno='',barcode='',track='',submitter='',contributor='',key='',secret=''):
        path = 'https://api.discogs.com/database/search'
        session.params['user-agent'] = self.unique_word
        session.params['q'] = q
        session.params['token'] = token
        session.params['title'] = title
        session.params['type'] = typee
        session.params['release_title'] = release_title
        session.params['credit'] = credit
        session.params['artist'] = artist
        session.params['anv'] = anv
        session.params['label'] = label
        session.params['genre'] = genre
        session.params['style'] = style
        session.params['country'] = country
        session.params['year'] = year
        session.params['format'] = formatt
        session.params['catno'] = catno
        session.params['barcode'] = barcode
        session.params['track'] = track
        session.params['submitter'] = submitter
        session.params['contributor'] = contributor
        session.params['key'] = key
        session.params['secret'] = secret

        response = session.get(path)
        return response.json()
        

    