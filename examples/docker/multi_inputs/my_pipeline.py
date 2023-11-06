from pipeline import Pipeline, Variable, pipe
from pipeline.objects.graph import InputField, InputSchema


class ChoicesSchema(InputSchema):
    choices_1: int = InputField(
        default=1,
        choices=[1, 2, 3],
        description="inner choices 1",
        title="sub_choice_1",
    )
    choices_2: str = InputField(
        default="ying",
        choices=["ying", "yang"],
        description="inner choices 2",
        title="sub_choice_2",
    )


@pipe
def predict(prompt: str, choices: ChoicesSchema) -> str:
    return f"{prompt}--{choices.choices_1}--{choices.choices_2}"


with Pipeline() as builder:
    prompt = Variable(str, title="prompt", default="Waifu baby", max_length=64)
    choices = Variable(ChoicesSchema)

    output = predict(prompt, choices)

    builder.output(output)

pipeline_graph = builder.get_pipeline()
