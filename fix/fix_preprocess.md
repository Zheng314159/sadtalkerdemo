"""
SadTalker\src\face3d\util\preprocess.py
只需要把原 align_img 替换为这个版本

"""

def align_img(img, lm, lm3D, mask=None, target_size=224.0, rescale_factor=102.0):
    """
    Return:
        trans_params       --numpy.array  (raw_W, raw_H, scale, tx, ty)
        img_new            --PIL.Image  (target_size, target_size, 3)
        lm_new             --numpy.array  (68, 2), y direction is opposite to v direction
        mask_new           --PIL.Image  (target_size, target_size)

    Parameters:
        img                --PIL.Image  (raw_H, raw_W, 3)
        lm                 --numpy.array  (68, 2)
        lm3D               --numpy.array  (5, 3)
        mask               --PIL.Image  (raw_H, raw_W, 3)
    """
    w0, h0 = img.size

    # 获取 5 点标记
    if lm.shape[0] != 5:
        lm5p = extract_5p(lm)
    else:
        lm5p = lm

    # 计算平移和缩放
    t, s = POS(lm5p.transpose(), lm3D.transpose())
    s = rescale_factor / s

    # resize & crop
    img_new, lm_new, mask_new = resize_n_crop_img(img, lm, t, s,
                                                  target_size=target_size, mask=mask)

    # 安全构造 trans_params
    def to_scalar(x):
        if isinstance(x, (list, tuple, np.ndarray)):
            arr = np.asarray(x).flatten()
            if arr.size == 0:
                return 0.0
            return float(arr[0])
        return float(x)

    trans_params = np.array([
        float(w0),
        float(h0),
        float(s),
        to_scalar(t[0]),
        to_scalar(t[1])
    ], dtype=float)

    return trans_params, img_new, lm_new, mask_new
