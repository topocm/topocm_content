c = get_config()

c.Exporter.preprocessors = ['cachedoutput.CachedOutputPreprocessor']
c.CachedOutputPreprocessor['enabled'] = True
