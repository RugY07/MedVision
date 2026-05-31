from flask import Blueprint, jsonify, current_app
import torch

models_bp = Blueprint('models', __name__)

@models_bp.route('/health', methods=['GET'])
def health_check():
    """
    Diagnostic status endpoint checking GPU hardware availability and loaded cache.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_manager = current_app.extensions['model_manager']
    
    return jsonify({
        'status': 'active',
        'device': device,
        'models_cached': list(model_manager.model_cache.keys()),
        'cuda_available': torch.cuda.is_available()
    }), 200


@models_bp.route('/models', methods=['GET'])
def models_status():
    """
    Provides statuses, target coefficients, classes, and descriptions of the 4 models.
    """
    model_manager = current_app.extensions['model_manager']
    status_list = []

    for key, meta in model_manager.model_metadata.items():
        is_cached = key in model_manager.model_cache
        
        status_list.append({
            'key': key,
            'name': meta['name'],
            'file_name': meta['file'],
            'loaded': is_cached,
            'device': str(model_manager.device) if is_cached else None,
            'classes': meta['classes']
        })

    return jsonify({
        'models': status_list
    }), 200
