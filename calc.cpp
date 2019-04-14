#include<iostream>
#include<cmath>
#include<vector>
#include<algorithm>
using namespace std;

const double PI = 2 * acos(0);
const double EPS = 1e-9;

#define ISEQUAL(a, b) (fabs(b - a) < EPS)

struct Pt {
    double x, y;

    Pt (double x = 0.0, double y = 0.0) {
        this->x = x;
        this->y = y;
    }
};

struct Vector {
    double x, y;

    Vector (double x = 0.0, double y = 0.0) {
        this->x = x;
        this->y = y;
    }

    bool operator == (const Vector& a) const {
        return (fabs(x - a.x) < EPS && fabs(y - a.y) < EPS);
    }

    bool operator != (const Vector& a) const {
        return !((*this) == a);
    }

    Vector operator - (const Vector& a) const {
        return Vector(x - a.x, y - a.y);
    }

    Vector operator / (const double& v) const {
        return Vector(x/v, y/v);
    }

    Vector operator * (const double& v) const {
        return Vector(x*v, y*v);
    }

    Vector operator + (const Vector& a) const {
        return Vector(x + a.x, y + a.y);
    }

    // scaller or dot product
    double operator * (const Vector& a) const {
        return (x*a.x + y*a.y);
    }

    // Vector or cross porduct
    double operator % (const Vector& a) const {
        return (x*a.y - y*a.x);
    }

    double squareDistance () {
        return ((*this)*(*this));
    }

    double value () {
        return sqrt((*this).squareDistance());
    }

    double angleWithXAxis () {
        double ang = atan2((*this).y, (*this).x);
        return ang + EPS < 0.0 ? ang + 2 * PI : ang;
    }
};

struct ScanLine {
    double ang;
    int obj_idx, pt_idx;

    ScanLine (double ang = 0.0, int obj_idx = 0, int pt_idx = 0) {
        this->ang = ang;e_dist = dist;

        this->obj_idx = obj_idx;
        this->pt_idx = pt_idx;
    }
};

struct Segment {
    Vector a, b;

    Segment (Vector a = Vector(0, 0), Vector b = Vector(0, 0)) {
        this->a = a;
        this->b = b;
    }

    double distanceFrom(Vector p) {
        if (((b - a) * (p - a)) + EPS < 0.0)
            return (p - a).value();
        else if (((a - b) * (p - b)) + EPS < 0.0)
            return (p - b).value();
        else {
            return fabs((b - a) % (p - a)) / (b - a).value();
        }
    }
};

struct Obj {
    int idx;
    double w, h;
    vector<Vector> pts;
    double enter_ang, leave_ang, visible_area;
    double attention;

    // (x1, y1) is the coordinate of lower-left corner of obj
    Obj (double x1 = 0.0, double y1 = 0.0, double w = 0.0, double h = 0.0, int idx = 0) {
        this->idx = idx;
        this->w = w;
        this->h = h;

        this->pts.push_back(Vector(x1, y1));
        this->pts.push_back(Vector(x1 + w, y1));
        this->pts.push_back(Vector(x1 + w, y1 + h));
        this->pts.push_back(Vector(x1, y1 + h));

        this->visible_area = 0.0;
    }

    double area() {
        return w * h;
    }

    void appendScanLines(vector<ScanLine> &ls, Vector face) {
        enter_ang = 1e9, leave_ang = -1e9;
        int p1, p2;
        double d1, d2;
        for (int i = 0; i < 4; i++) {
            double ang = (pts[i] - face).angleWithXAxis();
            if (enter_ang > ang) {
                enter_ang = ang;
                p1 = i;
            }

            if (leave_ang < ang) {
                leave_ang = ang;
                p2 = i;
            }
        }
        ls.push_back(ScanLine(enter_ang, idx, p1));
        ls.push_back(ScanLine(leave_ang, idx, p2));
    }

    double faceDist(Vector face) {
        double dist = 1e9;
        for (int i = 0; i < 4; i++) {
            dist = min(dist, Segment(pts[i], pts[(i + 1) % 4]).distanceFrom(face));
        }
        return dist;
    }

    double attentionDist(Vector face, Vector attention) {
        Vector center = Vector(pts[0].x + w / 2.0, pts[0].y + h / 2.0);
        return Segment(face, attention).distanceFrom(center);
    }
};

bool cmpScanLines(ScanLine a, ScanLine b) {
    return a.ang < b.ang;
}

struct line {
    double a, b, c;

    line() {}

    line(Vector p, Vector q) {
        a = p.y - q.y;
        b = q.x - p.x;
        c = - a * p.x - b * p.y;
    }
};

#define DET(a, b, c, d) (a * d - b * c)

Vector intersection_line(Vector a, Vector b, Vector c, Vector d) {
    line m = line(a, b);
    line n = line(c, d);
    double zn = DET(m.a, m.b, n.a, n.b);
    Vector res = Vector(- DET(m.c, m.b, n.c, n.b) / zn, - DET(m.a, m.c, n.a, n.c) / zn);

    return res;
}

vector<Vector> clipPolygon(Vector a, Vector b, vector<Vector> poly) {
    int sz_poly = poly.size();
    poly.push_back(poly[0]);

    vector<Vector> temp;
    for(int i = 0; i < sz_poly; i++) {
        double e = (b - a) % (poly[i] - a);
        double f = (b - a) % (poly[i + 1] - a);

        if(e + EPS > 0.0 && f + EPS > 0.0)
            temp.push_back(poly[i]);
        else if(e + EPS > 0.0 && f + EPS < 0.0) {
            temp.push_back(poly[i]);
            temp.push_back(intersection_line(poly[i], poly[i + 1], a, b));
        }
        else if(e + EPS < 0.0 && f + EPS > 0.0)
            temp.push_back(intersection_line(poly[i], poly[i + 1], a, b));
        //else if(e + eps < 0.0 && f + eps < 0.0)
    }

    return temp;
}

vector<Vector> clipObj(Vector face, Vector a, Vector b, vector<Vector> obj) {
    vector<Vector> clippedObj = clipPolygon(face, a, obj);
    return clipPolygon(b, face, clippedObj);
}

double polygonArea(vector<Vector> poly) {
    if(poly.empty())
        return 0.0;

    int sz_poly = poly.size();
    double res = 0.0;
    poly.push_back(poly[0]);
    for(int i = 0; i < sz_poly; i++) {
        res += (poly[i] % poly[i + 1]);
    }
    res /= 2.0;

    return fabs(res);
}

int main() {
    Vector face;
    cout << "enter face (x coord, y coord)...";
    cin >> face.x >> face.y;

    double view_ang1, view_ang2, x1, y1, x2, y2;
    cout << "enter face view angles ((x1, y1), (x2, y2))...";
    cin >> x1 >> y1 >> x2 >> y2;
    view_ang1 = (Vector(x1, y1) - face).angleWithXAxis();
    view_ang2 = (Vector(x2, y2) - face).angleWithXAxis();
    double attention_dir = (view_ang1 + view_ang2) / 2.0;

    int num_objs;
    vector<Obj> objs;
    cout << "enter number of objs...";
    cin >> num_objs;
    objs.resize(num_objs);

    vector<ScanLine> scan_lines;
    double w, h;
    cout << "enter the objs (lower-left x coord, lower-left y coord, width, height)...";
    for (int i = 0; i < num_objs; i++) {
        cin >> x1 >> y1 >> w >> h;

        objs[i] = Obj(x1, y1, w, h, i);
        objs[i].appendScanLines(scan_lines, face);
    }

    sort(scan_lines.begin(), scan_lines.end(), cmpScanLines);

    for (int i = 0; i < 2 * num_objs; i++) {
        if (i > 0) {
            int nearest_idx = -1;
            double min_dist = 1e9;
            for (int j = 0; j < num_objs; j++) {
                if (scan_lines[i].ang < objs[j].enter_ang + EPS ||
                    scan_lines[i - 1].ang + EPS > objs[j].leave_ang)
                    continue;

                double face_dist = objs[j].faceDist(face);
                if (min_dist > face_dist + EPS) {
                    min_dist = face_dist;
                    nearest_idx = j;
                }
            }
            if (nearest_idx == -1)
                continue;

            int o1 = scan_lines[i - 1].obj_idx, o2 = scan_lines[i].obj_idx;
            int i1 = scan_lines[i - 1].pt_idx, i2 = scan_lines[i].pt_idx;
            Vector p1 = objs[o1].pts[i1], p2 = objs[o2].pts[i2];
            objs[nearest_idx].visible_area += polygonArea(clipObj(face, p1, p2, objs[nearest_idx].pts));
        }
    }

    double total_attention = 0.0;
    for (int i = 0; i < num_objs; i++) {
        objs[i].attention = 1.0;
        objs[i].attention /= objs[i].attentionDist(face,
            (face + Vector(cos(attention_dir), sin(attention_dir))));
        objs[i].attention /= objs[i].faceDist(face);
        objs[i].attention *= objs[i].visible_area / (objs[i].area());

        total_attention += objs[i].attention;
    }

    for (int i = 0; i < num_objs; i++) {
        objs[i].attention *= (100.0 / total_attention);

        cout << "percentage attentaion of " << i << "th obj = " << objs[i].attention << "%%" << endl;
    }

    return 0;
}

/*
0 0
1 2 -1 2

5
-6 32 10 5
8 33 3 2
-10 40 5 3
5 37 5 3
1 45 16 5

0 0
1 2 -1 2

6
-6 32 10 5
8 33 3 2
-10 40 5 3
5 37 5 3
1 45 16 5
-5 20 12 5
*/