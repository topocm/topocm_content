c.Exporter.preprocessors = ['scripts.preprocessors.RemoveVersionPreprocessor',
                            'scripts.preprocessors.SetNamePreprocessor']
c.ClearOutputPreprocessor['enabled'] = True
c.RemoveVersionPreprocessor['enabled'] = True
c.ExecutePreprocessor['timeout'] = 3000
