// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#ifndef air_DebugApiServer_hpp
#define air_DebugApiServer_hpp

#include "ApiServerBase.hpp"
#include "common/common_utils/Utils.hpp"

namespace msr { namespace airlib {

    class DebugApiServer : public ApiServerBase {
    public:
		// env-gen
		bool unreal_reset_;

        virtual void start(bool block = false) override
        {
            common_utils::Utils::log("Debug server started");
        }
        virtual void stop() override
        {
            common_utils::Utils::log("Debug server stopped");
        }
        virtual ~DebugApiServer() override = default;

		// for environment generation
		virtual bool checkUnrealReset() override
		{
			return unreal_reset_;
		}

		virtual void setUnrealReset() override
		{
			unreal_reset_ = true;
		}

		virtual void unSetUnrealReset() override
		{
			unreal_reset_ = false;
		}
    };

}} //namespace
#endif
