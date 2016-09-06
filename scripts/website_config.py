c.Exporter.preprocessors = ['scripts.htmllinks.HtmlLinksPreprocessor', 'scripts.cachedoutput.CachedOutputPreprocessor', 'scripts.trust_preprocessor.TrustPreprocessor']
c.HtmlLinksPreprocessor['enabled'] = True
c.CachedOutputPreprocessor['enabled'] = True
c.CachedOutputPreprocessor.cache_directory = '.nb_output_cache'
c.CachedOutputPreprocessor.timeout = 300
c.TrustPreprocessor['enabled'] = True
