from urllib.parse import quote


api_key = "k_0vtefojw"

class AdvancedSearchInput:
    def __init__(self):
        self.title = None
        self.title_type = None
        self.release_date_from = None
        self.release_date_to = None
        self.user_rating_from = None
        self.user_rating_to = None
        self.number_of_votes_from = None
        self.number_of_votes_to = None
        self.genres = None
        self.title_groups = None
        self.title_data = None
        # self.companies = None
        # self.instant_watch_options = None
        # self.us_certificates = None
        # self.color_info = None
        # self.countries = None
        # self.countries_str = None
        self.keyword = None
        self.languages = None
        self.languages_str = None
        # self.filming_locations = None
        # self.popularity_from = None
        # self.popularity_to = None
        self.plot = None
        self.runtime_from = None
        self.runtime_to = None
        # self.sound_mix = None
        self.count = 1
        self.sort = None

    def to_query_string(self):
        query = ""
        if self.title is not None:
            query += f"&title={quote(self.title)}"
        if self.title_type is not None:
            query += f"&title_type={quote(self.title_type)}"
        if self.release_date_from is not None:
            query += f"&release_date_from={quote(self.release_date_from)}"
        if self.release_date_to is not None:
            query += f"&release_date_to={quote(self.release_date_to)}"
        if self.user_rating_from is not None:
            query += f"&user_rating_from={quote(str(self.user_rating_from))}"
        if self.user_rating_to is not None:
            query += f"&user_rating_to={quote(str(self.user_rating_to))}"
        if self.number_of_votes_from is not None:
            query += f"&number_of_votes_from={quote(str(self.number_of_votes_from))}"
        if self.number_of_votes_to is not None:
            query += f"&number_of_votes_to={quote(str(self.number_of_votes_to))}"
        if self.genres is not None:
            query += f"&genres={quote(self.genres)}"
        if self.title_groups is not None:
            query += f"&title_groups={quote(self.title_groups)}"
        if self.title_data is not None:
            query += f"&title_data={quote(self.title_data)}"
        # if self.companies is not None:
        #     query += f"&companies={quote(self.companies)}"
        # if self.instant_watch_options is not None:
        #     query += f"&instant_watch_options={quote(self.instant_watch_options)}"
        # if self.us_certificates is not None:
        #     query += f"&us_certificates={quote(self.us_certificates)}"
        # if self.color_info is not None:
        #     query += f"&color_info={quote(self.color_info)}"
        # if self.countries is not None:
        #     query += f"&countries={quote(self.countries)}"
        # if self.countries_str is not None:
        #     query += f"&countries_str={quote(self.countries_str)}"
        if self.keyword is not None:
            query += f"&keyword={quote(self.keyword)}"
        if self.languages is not None:
            query += f"&languages={quote(self.languages)}"
        if self.languages_str is not None:
            query += f"&languages_str={quote(self.languages_str)}"
        # if self.filming_locations is not None:
        #     query += f"&filming_locations={quote(self.filming_locations)}"
        # if self.popularity_from is not None:
        #     query += f"&popularity_from={quote(str(self.popularity_from))}"
        # if self.popularity_to is not None:
        #     query += f"&popularity_to={quote(str(self.popularity_to))}"
        if self.plot is not None:
            query += f"&plot={quote(self.plot)}"
        if self.runtime_from is not None:
            query += f"&runtime_from={quote(str(self.runtime_from))}"
        if self.runtime_to is not None:
            query += f"&runtime_to={quote(str(self.runtime_to))}"
        # if self.sound_mix is not None:
        #     query += f"&sound_mix={quote(self.sound_mix)}"
        # if self.count is not None:
        #     query += f"&count={quote(str(self.count))}"
        if self.count == 1:
            query += f"&count={quote(str(self.count))}"
        if self.sort is not None:
            query += f"&sort={quote(self.sort)}"

        if len(query) > 0:
            return f"https://imdb-api.com/API/AdvancedSearch/{api_key}/?{query[1:]}"  # remove leading "&" and prepend base_url
        else: return -1
