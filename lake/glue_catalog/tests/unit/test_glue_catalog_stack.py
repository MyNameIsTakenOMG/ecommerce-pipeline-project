import aws_cdk as core
import aws_cdk.assertions as assertions

from glue_catalog.glue_catalog_stack import GlueCatalogStack

# example tests. To run these tests, uncomment this file along with the example
# resource in glue_catalog/glue_catalog_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GlueCatalogStack(app, "glue-catalog")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
