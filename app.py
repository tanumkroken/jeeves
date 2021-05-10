#  Copyright (c) 2021 by Ole Christian Astrup. All rights reserved.  Licensed under MIT
#   license.  See LICENSE in the project root for license information.
#
from api import app
from ariadne import load_schema_from_path,  make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.queries import resolve_match_phrases, resolve_match_tokens, resolve_match_skill, resolve_spacy_meta, \
    resolve_is_english, \
    resolve_language,  resolve_analysis, resolve_wolfram_query, resolve_wolfram_voice, resolve_wolfram_check, \
    resolve_wolfram_conversation

from api.mutations import resolve_register_skill, resolve_register_domain

# The queries
query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("match_skill", resolve_match_skill)
query.set_field("match_phrases", resolve_match_phrases)
query.set_field("match_tokens", resolve_match_tokens)
query.set_field("spacy_meta", resolve_spacy_meta)
query.set_field("english", resolve_is_english)
query.set_field("language", resolve_language)
query.set_field("analysis", resolve_analysis)
query.set_field("wolfram_query", resolve_wolfram_query)
query.set_field("wolfram_voice", resolve_wolfram_voice)
query.set_field("wolfram_check", resolve_wolfram_check)
query.set_field("wolfram_conversation", resolve_wolfram_conversation)

# Mutations
mutation.set_field("register_skill", resolve_register_skill)
mutation.set_field("register_domain", resolve_register_domain)


type_defs = load_schema_from_path("./schemas/")
schema = make_executable_schema(type_defs, [query, mutation, snake_case_fallback_resolvers])



@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code



if __name__ == '__main__':
    app.run(debug=True)
    app.config.from_object('config') # Import settings from config.py
