#pragma once
#ifndef LOGOS_SERIALIZABLE_H
#define LOGOS_SERIALIZABLE_H

#include <map.h>
#include <string.h>

#include "logos_binary_object.h"

namespace logos {

  class LogosSerializable (

    virtual LogosBinaryObject
    deserialize(LogosBinaryObject & data,
                std::map<std::string, std::string> & settings);

    static virtual LogosSerializable
    fromJSON(std::string json_string,
              std::map<std::string, std::string> & settings);

    virtual LogosBinaryObject
    serialize(LogosBinaryObject & data,
              std::map<std::string, std::string> & settings);

    virtual std::string toJSON(std::map<std::string, std::string> & settings);

  )

}

#endif /* end of include guard: LOGOS_SERIALIZABLE_H */
