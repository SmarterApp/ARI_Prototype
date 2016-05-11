from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from pyramid.renderers import JSONP


from .models import (
    DBSession,
    Base,
    )

def db(request):
    maker = request.registry.dbmaker
    session = maker()
    
    def cleanup(request):
        session.close()
    request.add_finished_callback(cleanup)
    
    return session


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    #DBSession.configure(bind=engine)
    #Base.metadata.bind = engine
    
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
    
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    settings = config.registry.settings
    root_dir = settings['root.dir']

    config.add_static_view(name='js', path=root_dir+'/remus/remus/static/js')
    config.add_static_view(name='isaap', path=root_dir+'/remus/remus/static/isaap')
    config.add_static_view(name='ari3', path=root_dir+'/remus/remus/static/ari3')
    config.add_static_view(name='images', path=root_dir+'/remus/remus/static/images')

    config.add_renderer('jsonp', JSONP(param_name='callback'))
    
    
    config.add_route('api_login', '/api/login')
    config.add_view('remus.api.login', route_name='api_login')
    
    config.add_route('api_createSession', '/api/createSession')
    config.add_view('remus.api.createSession', route_name='api_createSession')

    config.add_route('api_convertToCSV', '/api/convertToCSV')
    config.add_view('remus.api.convertToCSV', route_name='api_convertToCSV')

    config.add_route('api_convertToCSVLegacy', '/api/convertToCSVLegacy')
    config.add_view('remus.api.convertToCSVLegacy', route_name='api_convertToCSVLegacy')

    config.add_route('api_saveToJSON', '/api/saveToJSON')
    config.add_view('remus.api.saveToJSON', route_name='api_saveToJSON', renderer='jsonp')

    config.add_route('api_itemStream', '/api/itemStream')
    config.add_view('remus.api.itemStream', route_name='api_itemStream')

    config.add_route('api_itemSave', '/api/itemSave')
    config.add_view('remus.api.itemSave', route_name='api_itemSave')

    config.add_route('controller', '/controller')
    config.add_view('remus.controller.controller', route_name='controller')


    ####### ari 
    config.add_route('api_ari_getAssessment', '/api/ari/getAssessment')
    config.add_view('remus.AriApi.getAssessment', route_name='api_ari_getAssessment',  renderer='string')

    config.add_route('api_ari_getItem', '/api/ari/getItem')
    config.add_view('remus.AriApi.getItem', route_name='api_ari_getItem')



    ###### end ari
    
    config.scan()
    return config.make_wsgi_app()
