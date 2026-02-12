import logging

from app.config import settings

logger = logging.getLogger(__name__)

_model = None


def get_model():
    """Lazy-load the sentence-transformers model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer

            _model = SentenceTransformer(settings.embedding_model)
            logger.info(f"Loaded embedding model: {settings.embedding_model}")
        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}")
            return None
    return _model


def generate_embedding(text: str) -> list[float] | None:
    """Generate a 384-dimensional embedding vector from text."""
    model = get_model()
    if model is None:
        return None
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return None


def generate_bean_embedding(
    flavor_notes: list[str],
    origin: str | None = None,
    process: str | None = None,
    description: str | None = None,
) -> list[float] | None:
    """Generate embedding for a bean from its characteristics."""
    parts = []
    if flavor_notes:
        parts.append(", ".join(flavor_notes))
    if origin:
        parts.append(origin)
    if process:
        parts.append(process)
    if description:
        parts.append(description)
    if not parts:
        return None
    text = ". ".join(parts)
    return generate_embedding(text)


def generate_review_embedding(
    flavor_notes: list[str],
    comment: str | None = None,
) -> list[float] | None:
    """Generate embedding for a review."""
    parts = []
    if flavor_notes:
        parts.append(", ".join(flavor_notes))
    if comment:
        parts.append(comment)
    if not parts:
        return None
    text = ". ".join(parts)
    return generate_embedding(text)
