
#include <cstdio>
#include <vector>
#include <list>
#include <tuple>
#include <iterator>
#include <algorithm>
#include <iostream>
#include "coordinate.hpp"

using namespace std;


template <typename T, typename const_iterator>
void poly2rec(const const_iterator& first, const const_iterator& last, std::vector< Rect<T> >& result);


int main()
{
    vector< Coor<int> > polygon;
    vector< Rect<int> > result;

    polygon.emplace_back(0, 1);
    polygon.emplace_back(0, 2);
    polygon.emplace_back(2, 2);
    polygon.emplace_back(2, 0);
    polygon.emplace_back(1, 0);
    polygon.emplace_back(1, 1);

    poly2rec(polygon.cbegin(), polygon.cend(), result);

    cout << "Rectangle list:\n";
    int i = 0;
    for (const auto& rect : result) {
        i++;
        cout << "Rectangle " << i << ": bl" << rect.getBL() << " " << "tr" << rect.getTR() << "\n";
    }

    return 0;
}

// rectangle: bottom_left (bl), top_left (tl), top_right (tr), bottom_right (br)
// return coordinates of a triangle for generating a rectangle: bottom_left (bl), bottom_right (br), top_left (tl)
template <typename const_iterator>
static auto findCoorTriangle(const const_iterator& first, const const_iterator& last) -> std::tuple<const_iterator, const_iterator, const_iterator>
{
    // find bottom_left (P_bl)
    const auto P_bl = std::min_element(first, last, [](const auto& lhs, const auto& rhs) -> bool {
                if (lhs.getY() != rhs.getY()) { return (lhs.getY() < rhs.getY()); }
                else { return (lhs.getX() < rhs.getX()); }
            });

    // find bottom_right P_br except P_bl
    const auto P_br = std::min_element(first, last, [&P_bl](const auto& lhs, const auto& rhs) -> bool {
                // skip the element P_bl
                if (lhs == (*P_bl)) { return false; }
                else if (rhs == (*P_bl)) { return true; }
                // find the smallest element
                else if (lhs.getY() != rhs.getY()) { return (lhs.getY() < rhs.getY()); }
                else { return (lhs.getX() < rhs.getX()); }
            });

    // find top_left P_tl
    const auto P_tl = std::min_element(first, last, [&P_bl, &P_br](const auto& lhs, const auto& rhs) -> bool {
                // skip the element (x, y) out of the range:
                // P_bl.getX() <= x < P_br.getX() && P_bl.getY() < y
                if ((lhs.getY() <= P_bl->getY()) || (lhs.getX() < P_bl->getX()) || (lhs.getX() >= P_br->getX())) { return false; }
                else if ((rhs.getY() <= P_bl->getY()) || (rhs.getX() < P_bl->getX()) || (rhs.getX() >= P_br->getX())) { return true; }
                // find the smallest element
                else if (lhs.getY() != rhs.getY()) { return (lhs.getY() < rhs.getY()); }
                else { return (lhs.getX() < rhs.getX()); }
                return true;
            });
            
    cout << "Coordinates for a triangle in a rectangle" << "\n";
    cout << "   P_bl: (x,y): (" << P_bl->getX() << ", " << P_bl->getY() << ")\n";
    cout << "   P_br: (x,y): (" << P_br->getX() << ", " << P_br->getY() << ")\n";
    cout << "   P_tl: (x,y): (" << P_tl->getX() << ", " << P_tl->getY() << ")\n";
    cout << "\n";

    return {P_bl, P_br, P_tl};
}


template <typename T>
static void updatePolygon(std::list< Coor<T> >& polygon, const Coor<T>& P_bl, const Coor<T>& P_br, const Coor<T>& P_tl)
{
    auto iter = polygon.begin();
    const Coor<T> up_left(P_bl.getX(), P_tl.getY()), up_right(P_br.getX(), P_tl.getY());
    bool insert_up_left = true, insert_up_right = true;

    // Update Policy:
    // 1. If the coordinate exists in the point array, then remove it from the point array
    // 2. Otherwise, add it into the point array
    while (iter != polygon.end()) {
        if (*iter == P_bl)        { iter = polygon.erase(iter); }
        else if (*iter == P_br)   { iter = polygon.erase(iter); }
        else if (*iter == up_left)  { iter = polygon.erase(iter); insert_up_left = false; }
        else if (*iter == up_right)  { iter = polygon.erase(iter); insert_up_right = false; }
        else                    { ++iter; }
    }

    if (insert_up_left) { polygon.emplace_back(up_left); }
    if (insert_up_right) { polygon.emplace_back(up_right); }
}


template <typename T, typename const_iterator>
void poly2rec(const const_iterator& first, const const_iterator& last, std::vector< Rect<T> >& result)
{
    std::list< Coor<T> > polygon(first, last);
    
    result.clear();
    while (polygon.size() > 0) {
        const auto& coord_triangle = findCoorTriangle(polygon.cbegin(), polygon.cend());
        const auto P_bl = *(std::get<0>(coord_triangle));
        const auto P_br = *(std::get<1>(coord_triangle));
        const auto P_tl = *(std::get<2>(coord_triangle));

        // extract rectangle
        result.emplace_back(P_bl.getX(), P_bl.getY(), P_br.getX() - P_bl.getX(), P_tl.getY() - P_bl.getY());

        // update polygon (point array)
        updatePolygon(polygon, P_bl, P_br, P_tl);
    }
}
