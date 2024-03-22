import pandas as pd
import numpy as np

from documentor.structuries.document import Document
from documentor.semantic.models.base import BaseSemanticModel


def cosine_similarity(vec1, vec2):
    """
    Calculate cos similarity between vectors

    :param vec1: first vector
    :type vec1: np.ndarray
    :param vec2: second vector.
    :type vec2: np.ndarray
    :return: cos distance between vectors
    :rtype: np.int
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def test_vectorization(vectorization_model, vectorize_example):
    similar = vectorize_example.similar_words
    dissimilar = vectorize_example.dissimilar_words
    similar_example = [vectorization_model.encode_word(word) for word in similar]
    dissimilar_example = [vectorization_model.encode_word(word) for word in dissimilar]

    assert abs(vectorize_example.similar_distance - cosine_similarity(*similar_example)) <= 0.2
    assert abs(vectorize_example.dissimilar_distance - cosine_similarity(*dissimilar_example)) <= 0.2
