c.Exporter.preprocessors = ['scripts.removeversion.RemoveVersionPreprocessor',
                            'scripts.removeversion.SetNamePreprocessor']
c.ClearOutputPreprocessor['enabled'] = True
c.RemoveVersionPreprocessor['enabled'] = True
