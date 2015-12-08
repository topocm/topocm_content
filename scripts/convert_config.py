import os
c = get_config()

c.Exporter.preprocessors = ['scripts.cachedoutput.CachedOutputPreprocessor']
c.CachedOutputPreprocessor['enabled'] = True
c.CachedOutputPreprocessor.cache_directory = os.path.abspath(".nb_output_cache")
