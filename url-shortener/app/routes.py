from flask import Blueprint, request, jsonify, redirect
from utils import generate_short_code, is_valid_url

router = Blueprint('router', __name__)

# In-memory data store
url_mapping = {}       # short_code -> original_url
click_counts = {}      # short_code -> click count

@router.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid or missing URL"}), 400

    # Generate unique short code
    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    url_mapping[short_code] = original_url
    click_counts[short_code] = 0

    return jsonify({
        "short_url": request.host_url + short_code,
        "original_url": original_url
    }), 201

@router.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        click_counts[short_code] += 1
        return redirect(original_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

@router.route('/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    if short_code in url_mapping:
        return jsonify({
            "original_url": url_mapping[short_code],
            "clicks": click_counts[short_code]
        })
    else:
        return jsonify({"error": "Short URL not found"}), 404
