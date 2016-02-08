c.Exporter.preprocessors = ['scripts.cachedoutput.CachedOutputPreprocessor']
c.CachedOutputPreprocessor['enabled'] = True
c.CachedOutputPreprocessor.cache_directory = '.nb_output_cache'
c.CachedOutputPreprocessor.req_files = ['code/init_mooc_nb.py',
                                        'code/edx_components.py',
                                        'code/pfaffian.py', 'code/functions.py']
c.CachedOutputPreprocessor.timeout = 300
