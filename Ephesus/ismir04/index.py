def get_indexes(track_ids, track_ids_in_order):
    indexes = []
    for track_id in track_ids:
        index = track_ids_in_order.index(track_id)
        indexes.append(index)
    return indexes