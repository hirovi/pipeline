from pipeline import Pipeline, entity, pipe


@entity
class MyPipelineEntity:
    @pipe(run_once=True, on_startup=True)
    def load(self):
        pass


with Pipeline() as builder:
    pass

pipeline_graph = builder.get_pipeline()
