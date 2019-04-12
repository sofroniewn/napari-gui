import numpy as np
from ...util import segment_normal
from vispy.geometry import PolygonData


def inside_triangles(triangles):
    """Checks which triangles contain the origin

    Parameters
    ----------
    triangles : np.ndarray
        Nx3x2 array of N triangles that should be checked

    Returns
    -------
    inside : np.ndarray
        Length N boolean array with `True` values for trinagles containg the
        origin
    """

    AB = triangles[:, 1, :] - triangles[:, 0, :]
    AC = triangles[:, 2, :] - triangles[:, 0, :]
    BC = triangles[:, 2, :] - triangles[:, 1, :]

    s_AB = -AB[:, 0]*triangles[:, 0, 1] + AB[:, 1]*triangles[:, 0, 0] >= 0
    s_AC = -AC[:, 0]*triangles[:, 0, 1] + AC[:, 1]*triangles[:, 0, 0] >= 0
    s_BC = -BC[:, 0]*triangles[:, 1, 1] + BC[:, 1]*triangles[:, 1, 0] >= 0

    inside = np.all(np.array([s_AB != s_AC, s_AB == s_BC]), axis=0)

    return inside


def inside_boxes(boxes):
    """Checks which boxes contain the origin. Boxes need not be axis aligned

    Parameters
    ----------
    boxes : np.ndarray
        Nx8x2 array of N boxes that should be checked

    Returns
    -------
    inside : np.ndarray
        Length N boolean array with `True` values for boxes containg the origin
    """

    AB = boxes[:, 0] - boxes[:, 6]
    AM = boxes[:, 0]
    BC = boxes[:, 6] - boxes[:, 4]
    BM = boxes[:, 6]

    ABAM = np.multiply(AB, AM).sum(1)
    ABAB = np.multiply(AB, AB).sum(1)
    BCBM = np.multiply(BC, BM).sum(1)
    BCBC = np.multiply(BC, BC).sum(1)

    c1 = 0 <= ABAM
    c2 = ABAM <= ABAB
    c3 = 0 <= BCBM
    c4 = BCBM <= BCBC

    inside = np.all(np.array([c1, c2, c3, c4]), axis=0)

    return inside


def triangles_intersect_box(triangles, corners):
    """Determines which triangles intersect an axis aligned box.

    Parameters
    ----------
    triangles : np.ndarray
        Nx3x2 array of vertices of triangles to be tested
    corners : np.ndarray
        2x2 array specifying corners of a box

    Returns
    -------
    intersects : np.ndarray
        Length N boolean array with `True` values for triangles intersecting
        the box
    """

    vertices_inside = triangle_vertices_inside_box(triangles, corners)
    edge_intersects = triangle_edges_intersect_box(triangles, corners)

    intersects = np.logical_or(vertices_inside, edge_intersects)

    return intersects


def triangle_vertices_inside_box(triangles, corners):
    """Determines which triangles have vertices inside an axis aligned box.

    Parameters
    ----------
    triangles : np.ndarray
        Nx3x2 array of vertices of triangles to be tested
    corners : np.ndarray
        2x2 array specifying corners of a box

    Returns
    -------
    inside : np.ndarray
        Length N boolean array with `True` values for triangles with
        vertices inside the box
    """
    box = create_box(corners)[[0, 4]]

    vertices_inside = np.empty(triangles.shape[:-1], dtype=bool)
    for i in range(3):
        # check if each triangle vertex is inside the box
        below_top = np.all(box[1] >= triangles[:, i, :], axis=1)
        above_bottom = np.all(triangles[:, i, :] >= box[0], axis=1)
        vertices_inside[:, i] = np.logical_and(below_top, above_bottom)

    inside = np.any(vertices_inside, axis=1)

    return inside


def triangle_edges_intersect_box(triangles, corners):
    """Determines which triangles have edges that intersect the edges of an
    axis aligned box.

    Parameters
    ----------
    triangles : np.ndarray
        Nx3x2 array of vertices of triangles to be tested
    corners : np.ndarray
        2x2 array specifying corners of a box

    Returns
    -------
    intersects : np.ndarray
        Length N boolean array with `True` values for triangles with
        edges that intersect the edges of the box.
    """
    box = create_box(corners)[[0, 2, 4, 6]]

    intersects = np.zeros([len(triangles), 12], dtype=bool)
    for i in range(3):
        # check if each triangle edge
        p1 = triangles[:, i, :]
        q1 = triangles[:, (i+1) % 3, :]

        for j in range(4):
            # Check the four edges of the box
            p2 = box[j]
            q2 = box[(j+1) % 3]
            intersects[:, i*3+j] = ([lines_intersect(p1[k], q1[k], p2, q2)
                                    for k in range(len(p1))])

    return np.any(intersects, axis=1)


def lines_intersect(p1, q1, p2, q2):
    """Determines if line segment p1q1 intersects line segment p2q2

    Parameters
    -------
    p1 : np.ndarray
        Length 2 array of first point of first line segment
    q1 : np.ndarray
        Length 2 array of second point of first line segment
    p2 : np.ndarray
        Length 2 array of first point of second line segment
    q2 : np.ndarray
        Length 2 array of second point of second line segment

    Returns
    -------
    intersects : bool
        Bool indicating if line segment p1q1 intersects line segment p2q2
    """
    # Determine four orientations
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Test general case
    if (o1 != o2) and (o3 != o4):
        return True

    # Test special cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    # p1, q1 and q2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    # Doesn't fall into any special cases
    return False


def on_segment(p, q, r):
    """Checks if q is on the segment from p to r

    Parameters
    -------
    p : np.ndarray
        Length 2 array of first point of segment
    q : np.ndarray
        Length 2 array of point to check if on segment
    r : np.ndarray
        Length 2 array of second point of segment

    Returns
    -------
    on : bool
        Bool indicating if q is on segment from p to r
    """
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        on = True
    else:
        on = False

    return on


def orientation(p, q, r):
    """Determines oritentation of ordered triplet (p, q, r)

    Parameters
    -------
    p : np.ndarray
        Length 2 array of first point of triplet
    q : np.ndarray
        Length 2 array of second point of triplet
    r : np.ndarray
        Length 2 array of third point of triplet

    Returns
    -------
    val : int
        One of (-1, 0, 1). 0 if p, q, r are colinear, 1 if clockwise, and -1
        if counterclockwise.
    """
    val = (q[1] - p[1])*(r[0] - q[0]) - (q[0] - p[0])*(r[1] - q[1])
    val = np.sign(val)

    return val


def point_to_lines(point, lines):
    """Calculate the distance between a point and line segments and returns the
    index of the closest line. First calculates the distance to the infinite
    line, then checks if the projected point lies between the line segment
    endpoints. If not, calculates distance to the endpoints

    Parameters
    ----------
    point : np.ndarray
        1x2 array of specifying the point
    lines : np.ndarray
        Nx2x2 array of line segments

    Returns
    -------
    index : int
        Integer index of the closest line
    location : float
        Normalized location of intersection of the distance normal to the line
        closest. Less than 0 means an intersection before the line segment
        starts. Between 0 and 1 means an intersection inside the line segment.
        Greater than 1 means an intersection after the line segment ends
    """

    # shift and normalize vectors
    lines_vectors = lines[:, 1] - lines[:, 0]
    point_vectors = point - lines[:, 0]
    end_point_vectors = point - lines[:, 1]
    norm_lines = np.linalg.norm(lines_vectors, axis=1, keepdims=True)
    reject = (norm_lines == 0).squeeze()
    norm_lines[reject] = 1
    unit_lines = lines_vectors / norm_lines

    # calculate distance to line
    line_dist = abs(np.cross(unit_lines, point_vectors))

    # calculate scale
    line_loc = (unit_lines*point_vectors).sum(axis=1)/norm_lines.squeeze()

    # for points not falling inside segment calculate distance to appropriate
    # endpoint
    line_dist[line_loc < 0] = np.linalg.norm(point_vectors[line_loc < 0],
                                             axis=1)
    line_dist[line_loc > 1] = np.linalg.norm(end_point_vectors[line_loc > 1],
                                             axis=1)
    line_dist[reject] = np.linalg.norm(point_vectors[reject], axis=1)
    line_loc[reject] = 0.5

    # calculate closet line
    index = np.argmin(line_dist)
    location = line_loc[index]

    return index, location


def create_box(data):
    """Creates the axis aligned interaction box of a list of points

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of points whose interaction box is to be found

    Returns
    -------
    box : np.ndarray
        9x2 array of vertices of the interaction box. The first 8 points are
        the corners and midpoints of the box in clockwise order starting in the
        upper-left corner. The last point is the center of the box
    """
    min_val = [data[:, 0].min(axis=0), data[:, 1].min(axis=0)]
    max_val = [data[:, 0].max(axis=0), data[:, 1].max(axis=0)]
    tl = np.array([min_val[0], min_val[1]])
    tr = np.array([max_val[0], min_val[1]])
    br = np.array([max_val[0], max_val[1]])
    bl = np.array([min_val[0], max_val[1]])
    box = np.array([tl, (tl+tr)/2, tr, (tr+br)/2, br, (br+bl)/2, bl, (bl+tl)/2,
                   (tl+tr+br+bl)/4])
    return box


def rectangle_to_box(data):
    """Converts the four corners of a rectangle into a interaction box like
    representation. If the rectangle is not axis aligned the resulting box
    representation will not be axis aligned either

    Parameters
    ----------
    data : np.ndarray
        4x2 array of corner points to be converted to a box like representation

    Returns
    -------
    box : np.ndarray
        9x2 array of vertices of the interaction box. The first 8 points are
        the corners and midpoints of the box in clockwise order starting in the
        upper-left corner. The last point is the center of the box
    """
    if not np.all(data.shape == (4, 2)):
        raise ValueError("""Data shape does not match expected `[4, 2]`
                         shape specifying corners for the rectangle""")
    box = np.array([data[0], (data[0]+data[1])/2, data[1], (data[1]+data[2])/2,
                    data[2], (data[2]+data[3])/2, data[3], (data[3]+data[0])/2,
                    data.mean(axis=0)])
    return box


def find_corners(data):
    """Finds the four corners of the interaction box definied by an array of
    points

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of points whose interaction box is to be found

    Returns
    -------
    corners : np.ndarray
        4x2 array of corners of the boudning box
    """
    min_val = [data[:, 0].min(axis=0), data[:, 1].min(axis=0)]
    max_val = [data[:, 0].max(axis=0), data[:, 1].max(axis=0)]
    tl = np.array([min_val[0], min_val[1]])
    tr = np.array([max_val[0], min_val[1]])
    br = np.array([max_val[0], max_val[1]])
    bl = np.array([min_val[0], max_val[1]])
    corners = np.array([tl, tr, br, bl])
    return corners


def center_radii_to_corners(center, radii):
    """Expands a center and radii into a four corner rectangle

    Parameters
    ----------
    center : np.ndarray | list
        Length 2 array or list of the center coordinates
    radii : np.ndarray | list
        Length 2 array or list of the two radii

    Returns
    -------
    corners : np.ndarray
        4x2 array of corners of the boudning box
    """
    data = np.array([center+radii, center-radii])
    corners = find_corners(data)
    return corners


def triangulate_ellipse(corners, num_segments=100):
    """Determines the triangulation of a path. The resulting `offsets` can
    mulitplied by a `width` scalar and be added to the resulting `centers`
    to generate the vertices of the triangles for the triangulation, i.e.
    `vertices = centers + width*offsets`. Using the `centers` and `offsets`
    representation thus allows for the computed triangulation to be
    independent of the line width.

    Parameters
    ----------
    corners : np.ndarray
        4x2 array of four bounding corners of the ellipse. The ellipse will
        still be computed properly even if the rectangle determined by the
        corners is not axis aligned
    num_segments : int
        Integer determining the number of segments to use when triangulating
        the ellipse

    Returns
    -------
    vertices : np.ndarray
        Mx2 array coordinates of vertices for triangulating an ellipse.
        Includes the center vertex of the ellipse, followed by `num_segments`
        vertices around the boundary of the ellipse
    triangles : np.ndarray
        Px2 array of the indices of the vertices for the triangles of the
        triangulation. Has length given by `num_segments`
    """
    if not np.all(corners.shape == (4, 2)):
        raise ValueError("""Data shape does not match expected `[4, 2]`
                         shape specifying corners for the ellipse""")

    center = corners.mean(axis=0)
    adjusted = corners - center

    vec = adjusted[1] - adjusted[0]
    len_vec = np.linalg.norm(vec)
    if len_vec > 0:
        # rotate to be axis aligned
        norm_vec = vec/len_vec
        transform = np.array([[norm_vec[0], -norm_vec[1]],
                             [norm_vec[1], norm_vec[0]]])
        adjusted = np.matmul(adjusted, transform)
    else:
        transform = np.eye(2)

    radii = abs(adjusted[0])
    vertices = np.zeros((num_segments + 1, 2), dtype=np.float32)
    theta = np.linspace(0, np.deg2rad(360), num_segments)
    vertices[1:, 0] = radii[0] * np.cos(theta)
    vertices[1:, 1] = radii[1] * np.sin(theta)

    if len_vec > 0:
        # rotate back
        vertices = np.matmul(vertices, transform.T)

    # Shift back to center
    vertices = vertices + center

    triangles = np.array([[0, i+1, i+2] for i in range(num_segments)])
    triangles[-1, 2] = 1

    return vertices, triangles


def triangulate_face(data):
    """Determines the triangulation of the face of a shape.

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of vertices of shape to be triangulated

    Returns
    -------
    vertices : np.ndarray
        Mx2 array vertices of the trinagles.
    triangles : np.ndarray
        Px3 array of the indices of the vertices that will form the
        triangles of the triangulation
    """
    vertices, triangles = PolygonData(vertices=data).triangulate()
    triangles = triangles.astype(np.uint32)

    return vertices, triangles


def triangulate_edge(path, closed=False, limit=3, bevel=False):
    """Determines the triangulation of a path. The resulting `offsets` can
    mulitplied by a `width` scalar and be added to the resulting `centers`
    to generate the vertices of the triangles for the triangulation, i.e.
    `vertices = centers + width*offsets`. Using the `centers` and `offsets`
    representation thus allows for the computed triangulation to be
    independent of the line width.

    Parameters
    ----------
    path : np.ndarray
        Nx2 array of central coordinates of path to be triangulated
    closed : bool
        Bool which determines if the path is closed or not
    limit : float
        Miter limit which determines when to switch from a miter join to a
        bevel join
    bevel : bool
        Bool which if True causes a bevel join to always be used. If False
        a bevel join will only be used when the miter limit is exceeded

    Returns
    -------
    centers : np.ndarray
        Mx2 array central coordinates of path trinagles.
    offsets : np.ndarray
        Mx2 array of the offests to the central coordinates that need to
        be scaled by the line width and then added to the centers to
        generate the actual vertices of the triangulation
    triangles : np.ndarray
        Px3 array of the indices of the vertices that will form the
        triangles of the triangulation
    """
    # Remove any equal adjacent points
    if len(path) > 2:
        clean_path = np.array([p for i, p in enumerate(path) if i == 0 or
                              not np.all(p == path[i-1])])
    else:
        clean_path = path

    if closed:
        if np.all(clean_path[0] == clean_path[-1]) and len(clean_path) > 2:
            clean_path = clean_path[:-1]
        full_path = np.concatenate(([clean_path[-1]], clean_path,
                                    [clean_path[0]]), axis=0)
        normals = ([segment_normal(full_path[i], full_path[i+1]) for i in
                   range(len(clean_path))])
        path_length = ([np.linalg.norm(full_path[i]-full_path[i+1]) for i in
                       range(len(clean_path))])
        normals = np.array(normals)
        full_path = np.concatenate((clean_path, [clean_path[0]]), axis=0)
        full_normals = np.concatenate((normals, [normals[0]]), axis=0)
    else:
        full_path = np.concatenate((clean_path, [clean_path[-2]]), axis=0)
        normals = ([segment_normal(full_path[i], full_path[i+1]) for i in
                   range(len(clean_path))])
        path_length = ([np.linalg.norm(full_path[i]-full_path[i+1]) for i in
                       range(len(clean_path))])
        normals[-1] = -normals[-1]
        normals = np.array(normals)
        full_path = clean_path
        full_normals = np.concatenate(([normals[0]], normals), axis=0)

    miters = np.array([full_normals[i:i+2].mean(axis=0) for i in
                      range(len(full_path))])
    miters = np.array([miters[i]/np.dot(miters[i], full_normals[i])
                      if np.dot(miters[i], full_normals[i]) != 0
                      else full_normals[i] for i in range(len(full_path))])
    miter_lengths = np.linalg.norm(miters, axis=1)
    miters = 0.5*miters
    vertex_offsets = []
    central_path = []
    triangles = []
    m = 0

    for i in range(len(full_path)):
        if i == 0:
            if (bevel or miter_lengths[i] > limit) and closed:
                offset = np.array([miters[i, 1], -miters[i, 0]])
                offset = 0.5*offset/np.linalg.norm(offset)
                flip = np.sign(np.dot(offset, full_normals[i]))
                vertex_offsets.append(offset)
                vertex_offsets.append(-flip*miters[i]/miter_lengths[i]*limit)
                vertex_offsets.append(-offset)
                central_path.append(full_path[i])
                central_path.append(full_path[i])
                central_path.append(full_path[i])
                triangles.append([0, 1, 2])
                m = m+1
            else:
                vertex_offsets.append(-miters[i])
                vertex_offsets.append(miters[i])
                central_path.append(full_path[i])
                central_path.append(full_path[i])
        elif i == len(full_path)-1:
            if closed:
                a = vertex_offsets[m+1]
                b = vertex_offsets[1]
                ray = full_path[i] - full_path[i-1]
                if np.cross(a, ray)*np.cross(b, ray) > 0:
                    triangles.append([m, m+1, 1])
                    triangles.append([m, 0, 1])
                else:
                    triangles.append([m, m+1, 1])
                    triangles.append([m+1, 0, 1])
            else:
                vertex_offsets.append(-miters[i])
                vertex_offsets.append(miters[i])
                central_path.append(full_path[i])
                central_path.append(full_path[i])
                a = vertex_offsets[m+1]
                b = vertex_offsets[m+3]
                ray = full_path[i] - full_path[i-1]
                if np.cross(a, ray)*np.cross(b, ray) > 0:
                    triangles.append([m, m+1, m+3])
                    triangles.append([m, m+2, m+3])
                else:
                    triangles.append([m, m+1, m+3])
                    triangles.append([m+1, m+2, m+3])
        elif (bevel or miter_lengths[i] > limit):
            offset = np.array([miters[i, 1], -miters[i, 0]])
            offset = 0.5*offset/np.linalg.norm(offset)
            flip = np.sign(np.dot(offset, full_normals[i]))
            vertex_offsets.append(offset)
            vertex_offsets.append(-flip*miters[i]/miter_lengths[i]*limit)
            vertex_offsets.append(-offset)
            central_path.append(full_path[i])
            central_path.append(full_path[i])
            central_path.append(full_path[i])
            a = vertex_offsets[m+1]
            b = vertex_offsets[m+3]
            ray = full_path[i] - full_path[i-1]
            if np.cross(a, ray)*np.cross(b, ray) > 0:
                triangles.append([m, m+1, m+3])
                triangles.append([m, m+2, m+3])
            else:
                triangles.append([m, m+1, m+3])
                triangles.append([m+1, m+2, m+3])
            triangles.append([m+2, m+3, m+4])
            m = m + 3
        else:
            vertex_offsets.append(-miters[i])
            vertex_offsets.append(miters[i])
            central_path.append(full_path[i])
            central_path.append(full_path[i])
            a = vertex_offsets[m+1]
            b = vertex_offsets[m+3]
            ray = full_path[i] - full_path[i-1]
            if np.cross(a, ray)*np.cross(b, ray) > 0:
                triangles.append([m, m+1, m+3])
                triangles.append([m, m+2, m+3])
            else:
                triangles.append([m, m+1, m+3])
                triangles.append([m+1, m+2, m+3])
            m = m + 2
    centers = np.array(central_path)
    offsets = np.array(vertex_offsets)
    triangles = np.array(triangles)

    return centers, offsets, triangles
