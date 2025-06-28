

class MediaCache:
    '''
    A
        obtains media of given URL and returns details of specified item including the file location that can be played.
        Additionally it provides quick subsequent access by caching a copy upon first access.
        i.e. do it all

    '''

    def __init__(self, metadata_dir, media_dir):
        self.metadata_dir = metadata_dir
        self.media_dir = media_dir

    def list_entries(self):
        return None

    def clear_all_entries(self):
        return None

    def get_entry_details(self, url):
        '''
        provides details of whether the given URL has
        :param url:
        :return: (url, Status(unavailable, in progress), Title, Duration, when downloaded)
        '''
        return None

    def clear_entry(self, url):
        '''
        Delete the specified URL
        :param url:
        :return: Bool True==Existed, False==Not exist
        '''
        return None

    def check_network(self):
        return None

    def pull_entry(self, url):
        '''
        Request the media for the specified URL be downloaded locally.
        :param url:
        :return: Bool True==Media found and is being actioned , False== Media does not exist Or problem downloading
        '''
        return None

