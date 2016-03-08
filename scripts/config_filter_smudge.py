c.Exporter.preprocessors = ['scripts.cachedoutput.CachedOutputPreprocessor', 'scripts.sign_nb_preprocessor.SignNBPreprocessor']
c.CachedOutputPreprocessor['enabled'] = True
c.CachedOutputPreprocessor.cache_directory = '.nb_output_cache'
c.CachedOutputPreprocessor.req_files = ['code/init_mooc_nb.py',
                                        'code/edx_components.py',
                                        'code/pfaffian.py', 'code/functions.py']
c.CachedOutputPreprocessor.timeout = 300
c.SignNBPreprocessor['enabled'] = True
